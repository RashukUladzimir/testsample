from django.contrib import admin
from django.db.models import F
from django.urls import reverse

from bboard.forms import AdForm
from bboard.models import Ad, Spare, Machine, Rubric


class PriceListFilter(admin.SimpleListFilter):
    title = 'Price'
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        return (
            ('low', 'low price'),
            ('high', 'high price'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(price__lt=100)
        if self.value() == 'high':
            return queryset.filter(price__gt=1000)


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'price', 'rubric', 'rubric_name']
    list_display_links = []

    list_select_related = ['rubric', ]
    ordering = ['id', ]
    empty_value_display = '-----'
    search_fields = ['^title', '=content', 'price']

    show_full_result_count = True

    list_filter = ['title', 'rubric__name', PriceListFilter]

    def discount(self, request, queryset):
        f_price = F('price')
        for obj in queryset:
            obj.price = f_price/2
            obj.save()
        self.message_user(request, 'Action was made')

    discount.short_description = 'Divide price by 2'

    actions = (discount, )
    actions_on_top = True
    actions_selection_counter = False

    def rubric_name(self, obj):
        if not obj:
            return None
        if not obj.rubric:
            return None
        return obj.rubric.name
    rubric_name.empty_value_display = '^'

    readonly_fields = ['content',]

    def get_fields(self, request, obj=None):
        fields = ['title', 'price', 'content']
        if not obj:
            fields.append('rubric')
        return fields

    fieldsets = (
        (None, {
            'fields': ('title', 'rubric', 'price'),

        }),
        ('Additional information', {
            'fields': ('content',),
            'description': 'Params without need to fill'
        }),
    )

    form = AdForm


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    fields = ('name', 'spares')

    filter_vertical = ('spares',)

    save_as = True
    save_as_continue = False


class AdInline(admin.TabularInline):
    model = Ad
    extra = 0

    can_delete = False
    show_change_link = False

    verbose_name = 'Reklama'
    verbose_name_plural = 'Reklami'


@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
    inlines = [AdInline,]
