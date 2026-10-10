from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import (
    Message,
    Conversation,
    ConversationMember
)
from accounts.models import User, UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from .forms import CreateGroupForm, EditProfileForm
# Create your views here.


class HomeView(LoginRequiredMixin, View):
    template_name = "chat/home.html"

    def get(self, request):
        conversations_groups = Conversation.objects.filter(type="group", conversations__user = request.user)
        conversations_privats = Conversation.objects.filter(type="privat", conversations__user = request.user)
        global_groups = Conversation.objects.filter(type="group").exclude(conversations__user = request.user)

        for i in global_groups:
            print("=========================",i.group_name)

        return render(request, self.template_name, {
            "groups":conversations_groups, "privats":conversations_privats,
            "globals":global_groups
            })

class GroupChatView(LoginRequiredMixin, View):
    template_name = "chat/group_chat.html"

    def setup(self, request, *args, **kwargs):
        self.group = get_object_or_404(Conversation, type="group", id = kwargs["room_id"])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        group = self.group
        user = request.user
        
        if not group.conversations.filter(user = user).exists():
            ConversationMember.objects.create(user=request.user, conversation=group)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        messages = self.group.messages.select_related("user")
        return render(request, self.template_name, {"group":self.group, "messages":messages})

class PrivatChatView(LoginRequiredMixin, View):
    template_name = "chat/privat_chat.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.other_user = get_object_or_404(User, id=kwargs["user_id"])
        self.conversation = (
            Conversation.objects
            .filter(type="privat")
            .filter(conversations__user=request.user)
            .filter(conversations__user=self.other_user)
            .first()
        )

    def dispatch(self, request, *args, **kwargs):
        if self.other_user == request.user:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if not self.conversation:
            self.conversation = Conversation.objects.create(type="privat")
            ConversationMember.objects.create(user=request.user, conversation=self.conversation)
            ConversationMember.objects.create(user=self.other_user, conversation=self.conversation)

        messages = self.conversation.messages.select_related("user").order_by("created")

        return render(request, self.template_name, {
            "conversation": self.conversation,
            "other_user": self.other_user,
            "messages": messages,
        })

class CreateGroupView(LoginRequiredMixin, View):
    template_name = "chat/create_group.html"
    form_class = CreateGroupForm

    def get(self, request):
        return render(request, self.template_name, {"form":self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            conv = Conversation.objects.create(type="group", group_name = name)
            ConversationMember.objects.create(user = request.user, conversation = conv)
            return redirect("home")
        return render(request, self.template_name, {"form":form})

class UserProfileView(View):
    template_name = "chat/profile.html"

    def setup(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, id=kwargs["user_id"])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if self.user != request.user:
            return redirect("login_page")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_id):
        user = self.user
        return render(request, self.template_name, {"user":user})

class EditProfileView(View):
    template_name = "chat/edit_profile.html"
    form_class = EditProfileForm

    def setup(self, request, *args, **kwargs):
        self.profile = get_object_or_404(UserProfile, user__id = kwargs["user_id"])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if self.profile.user != request.user:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance = self.profile)
        return render(request, self.template_name, {"form":form, "profile":self.profile})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        profile = self.profile
        if form.is_valid():
            cd = form.cleaned_data
            profile.user = request.user
            profile.username_id = cd["username_id"]
            profile.bio = cd["bio"]
            profile.profile = cd["profile"]
            profile.age = cd["age"]
            profile.date_of_birth = cd["date_of_birth"]
            profile.save()
            return redirect("home")
        return render(request, self.template_name, {"form":form})

