from django.db import models


class TGUser(models.Model):
    id = models.BigIntegerField(primary_key=True, verbose_name="User ID")
    chat_id = models.BigIntegerField(verbose_name="Chat ID")
    username = models.CharField(
        max_length=64, null=True, verbose_name="Username"
    )

    objects: models.manager.BaseManager["TGUser"]

    class Meta:
        db_table = "tg_user"


class TGBot(models.Model):
    bot_on = models.BooleanField(default=True, verbose_name="On/Off")
    admin = models.BooleanField(default=False, verbose_name="Admin")
    id = models.CharField(max_length=60, primary_key=True, verbose_name="Bot Token")
    bot_username = models.CharField(max_length=64, null=True, verbose_name="Bot Username")
    it_department_owner = models.CharField(max_length=64, null=False, verbose_name="IT Department Owner")

    objects: models.manager.BaseManager["TGBot"]

    def __unicode__(self):
        return self.bot_username

    def __str__(self):
        return self.bot_username

    class Meta:
        db_table = "tg_bot"
        verbose_name = 'Bot'
        verbose_name_plural = 'Bots'


class TGChat(models.Model):
    GROUP = 'Group'
    CHANNEL = 'Channel'
    CHAT_TYPE = [
        (GROUP, 'Group'),
        (CHANNEL, 'Channel'),
    ]
    id = models.BigIntegerField(primary_key=True, verbose_name="ID")
    chat_title = models.CharField(max_length=64, null=True, verbose_name="Title")
    id_bot = models.ForeignKey(TGBot, on_delete=models.DO_NOTHING, null=False, verbose_name="Message Listening Bot")
    chat_type = models.CharField(max_length=10, choices=CHAT_TYPE, default=CHANNEL,
                                 null=True, verbose_name="Chat Type")
    objects: models.manager.BaseManager["TGChat"]

    def __unicode__(self):
        return self.chat_title

    def __str__(self):
        return self.chat_title

    class Meta:
        db_table = "tg_chat"
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'


class TGLabel(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    label = models.CharField(max_length=50, null=True, verbose_name="Label")

    objects: models.manager.BaseManager["TGLabel"]

    class Meta:
        db_table = "tg_label"
        verbose_name = 'Label Post Processing Msg'
        verbose_name_plural = 'Labels Post Processing Msg'

    def __unicode__(self):
        return self.label

    def __str__(self):
        return self.label


class TGTemplateParseMsg(models.Model):
    INCLUDE = 'In'
    EXCLUDE = 'Ex'
    CONDITION_TYPE = [
        (INCLUDE, 'Include'),
        (EXCLUDE, 'Exclude'),
    ]
    NULL = ''
    COUNTER_UNIQ = 'Counter Uniq'
    COLLECTOR_VALUE = 'Collector Value'
    REPORT_TYPE = [
        (COUNTER_UNIQ, 'Counter Uniq'),
        (COLLECTOR_VALUE, 'Collector Value'),
        (NULL, ''),
    ]
    template_on = models.BooleanField(default=True, verbose_name="On/Off")
    priority = models.IntegerField(null=False, verbose_name="Priority")
    condition_type = models.CharField(max_length=2, choices=CONDITION_TYPE, default=INCLUDE,
                                      null=True, verbose_name="In/Exclude")
    report_type = models.CharField(max_length=30, choices=REPORT_TYPE, default=NULL, null=True, blank=True,
                                   verbose_name="Report")
    id = models.AutoField(primary_key=True, verbose_name="ID")
    id_label = models.ForeignKey(TGLabel, on_delete=models.DO_NOTHING, verbose_name="Label")
    id_chat = models.ForeignKey(TGChat, on_delete=models.DO_NOTHING, verbose_name="Chat")
    description = models.CharField(max_length=80, null=True, verbose_name="Descript")
    regex = models.TextField(max_length=200, null=True, verbose_name="RegexName")
    replace = models.CharField(max_length=80, null=False, verbose_name="ReplName")
    value_regex = models.TextField(max_length=100, null=True, blank=True, verbose_name="RegexVal")
    value_eq = models.CharField(max_length=80, null=True, blank=True, verbose_name="ValueEq")

    objects: models.manager.BaseManager["TGTemplateParseMsg"]

    class Meta:
        db_table = "tg_template_parse_msg"
        verbose_name = 'Template Parse Msg'
        verbose_name_plural = 'Template Parse Msgs'


class TGRawMessage(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    id_tg_msg = models.BigIntegerField(default=0, verbose_name="ID Telegram Msg")
    chat_id = models.BigIntegerField(null=False, verbose_name="Chat ID")
    chat_name = models.CharField(max_length=64, null=True, verbose_name="Chat Name")
    username = models.CharField(max_length=64, null=True, verbose_name="Username")
    raw_message = models.TextField(null=True, verbose_name="Raw Text Message")
    date_time = models.DateTimeField(null=True, verbose_name="Create Datetime")

    objects: models.manager.BaseManager["TGRawMessage"]

    class Meta:
        db_table = "tg_raw_message"
        verbose_name = 'RAW-message'
        verbose_name_plural = 'RAW-messages'


class TGInlineKeyboardButton(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    id_bot = models.ForeignKey(TGBot, on_delete=models.DO_NOTHING, null=False, verbose_name="Bot")
    id_chat = models.ForeignKey(TGChat, on_delete=models.DO_NOTHING, verbose_name="Chat")
    button_text = models.CharField(max_length=50, null=True, verbose_name="Button Text")
    callback_data = models.CharField(max_length=30, null=True, verbose_name="Callback data")
    labels = models.ForeignKey(TGLabel, on_delete=models.DO_NOTHING, verbose_name="Label")
    admin = models.BooleanField(default=False, verbose_name="Admin")

    objects: models.manager.BaseManager["TGInlineKeyboardButton"]

    class Meta:
        db_table = "tg_inline_keyboard_button"
        verbose_name = 'Command Button'
        verbose_name_plural = 'Command Buttons'


class TGMessage(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    id_tg_msg = models.BigIntegerField(default=0, verbose_name="ID Telegram Msg")
    chat_id = models.BigIntegerField(null=False, verbose_name="Chat ID")
    chat_name = models.CharField(max_length=64, null=True, verbose_name="Chat")
    username = models.CharField(max_length=64, null=True, verbose_name="Username")
    message = models.CharField(max_length=128, null=True, verbose_name="Message")
    value_float = models.FloatField(null=True, blank=True, verbose_name="ValueFloat")
    value_str = models.CharField(max_length=128, null=True, blank=True, verbose_name="ValueStr")
    label = models.CharField(max_length=64, null=True, verbose_name="Label")
    id_template = models.IntegerField(null=False, verbose_name="Template")
    date_time = models.DateTimeField(null=True, verbose_name="Create Datetime")

    objects: models.manager.BaseManager["TGMessage"]

    class Meta:
        db_table = "tg_message"
        verbose_name = 'Post Processed Message'
        verbose_name_plural = 'Post Processed Messages'

