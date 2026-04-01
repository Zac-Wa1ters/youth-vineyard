from django.db import models

from modelcluster.fields import ParentalKey


from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet

from wagtail.contrib.settings.models import BaseSiteSetting, register_setting


from django import forms


@register_setting
class SnipcartSettings(BaseSiteSetting):
    api_key = models.CharField(
        max_length=255,
        help_text='Your Snipcart public API key'
    )
        
@register_snippet
class SiteBranding(models.Model):
    organization_name = models.CharField(max_length=150, default="Youth Vineyard")
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("organization_name"),
        FieldPanel("logo"),
    ]

    def __str__(self):
        return self.organization_name
    
@register_snippet
class SiteFooter(models.Model):
    footer_text = RichTextField(blank=True)
    contact_text = models.CharField(max_length=100, blank=True, default="Contact")
    contact_link = models.URLField(blank=True)

    panels = [
        FieldPanel("footer_text"),
        FieldPanel("contact_text"),
        FieldPanel("contact_link"),
    ]

    def __str__(self):
        return "Site Footer"

class AboutPage(Page): 

    hero_title= models.CharField(max_length=255)
    hero_image=models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    organization_story = RichTextField()
    founder_bio = RichTextField()
    mission_statement = RichTextField()
    mentalhealth_services = RichTextField()
    donate = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("hero_image"),
        FieldPanel("organization_story"),
        FieldPanel("founder_bio"),
        FieldPanel("mission_statement"),
        FieldPanel("mentalhealth_services"),
        FieldPanel("donate")
    ]



class KeynotePage(Page): 

    hero_title= models.CharField(max_length=255)
    hero_image=models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    keynote_speaking = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("hero_image"),
        FieldPanel("keynote_speaking")
    ]


class GalleryIndexPage(Page): #for rendering the entire gallery in a grid 
    template = "app/gallery_index_page.html"
    parent_page_types = ["app.LandingPage"] #what ever file is rendering the home page nav bar
    subpage_types = ["app.GalleryEventPage"] #any children pages inside the index
    content_panels = Page.content_panels

class GalleryEventPage(Page): #when you click on one event in gallery
    template = "app/gallery_event_page.html"

    date = models.DateField()
    description = RichTextField()

    hero_image = models.ForeignKey(
            "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    video_url = models.URLField(blank=True)
    parent_page_types = ["app.GalleryIndexPage"]
    

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("description"),
        FieldPanel("hero_image"),
        FieldPanel("video_url"),
        InlinePanel("gallery_images", label = "Gallery Images"),
        InlinePanel("gallery_videos", label = "Gallery Videos")


    ]

class GalleryImagePage(Orderable):
    page = ParentalKey(
        'GalleryEventPage',
        on_delete = models.CASCADE,
        related_name = "gallery_images"
    )
    image=models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    panels = [FieldPanel('image')]

class GalleryVideoPage(Orderable):
    page = ParentalKey(
        'GalleryEventPage',
        on_delete = models.CASCADE,
        related_name = "gallery_videos"
    )
    video_url = models.URLField(blank=True, null=True)
    panels = [FieldPanel('video_url')]
    

class EventPage(Page): 
    
    sku = models.CharField(max_length=255, blank=True, null=True)
    event_date = models.DateField()
    event_time = models.TimeField()
    venue_name = models.CharField(max_length=255)
    event_description = RichTextField()
    is_quad_cities = models.BooleanField(
        default=False,
        help_text="Check if this event takes place in the Quad Cities. Leave unchecked for Water Valley.")

    content_panels = Page.content_panels + [
        FieldPanel("sku"),
        FieldPanel("event_date"),
        FieldPanel("event_time"),
        FieldPanel("venue_name"),
        FieldPanel("event_description"),
        FieldPanel("is_quad_cities", heading="Region"),

        InlinePanel("ticket_types", label="Ticket Types"),
    ]

class EventTicketType(Orderable):
    event = ParentalKey(
        "app.EventPage",
        related_name="ticket_types",
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    tickets_available = models.PositiveBigIntegerField(null=True)
    sku = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )


    FieldPanels = [
        FieldPanel("name"),
        FieldPanel("price"),
        FieldPanel("tickets_available"),
        FieldPanel("sku")
    ]
            

class EventIndexPage(Page): #This loops through EventPage and gets all the info to render on the Box Office Page. 
    
   def get_context(self, request):
    context = super().get_context(request)

    events = EventPage.objects.child_of(self).live().order_by("event_date")

    region = request.GET.get("region", "water_valley")

    if region == "quad_cities":
        events = events.filter(is_quad_cities=True)
    else:
        events = events.filter(is_quad_cities=False)

    context["events"] = events
    context["active_region"] = region

    return context



class LandingPage(Page):
    
    title_text = models.CharField(max_length=250, blank=True)
    quote = models.CharField(max_length=250, blank=True)
    main_image = models.ForeignKey(
                                "wagtailimages.Image",
                                null=True,
                                blank=True,
                                on_delete=models.SET_NULL,
                                related_name="+",
                                )
    
    preview_header = models.CharField(max_length=250, blank=True)
    
    preview_image_1 = models.ForeignKey(
                                "wagtailimages.Image",
                                null=True,
                                blank=True,
                                on_delete=models.SET_NULL,
                                related_name="+",)

    preview_image_2 = models.ForeignKey(
                                "wagtailimages.Image",
                                null=True,
                                blank=True,
                                on_delete=models.SET_NULL,
                                related_name="+",)

    preview_image_3 = models.ForeignKey(
                                "wagtailimages.Image",
                                null=True,
                                blank=True,
                                on_delete=models.SET_NULL,
                                related_name="+",)
    
    gallery_button_text = models.CharField(max_length=100, blank=True)
    gallery_button_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    

    more_info_header = models.CharField(max_length=100, blank=True)    
    more_info_text = RichTextField(blank=True)
    more_info_image =  models.ForeignKey(
                                "wagtailimages.Image",
                                null=True,
                                blank=True,
                                on_delete=models.SET_NULL,
                                related_name="+",)
    
    info_button_text = models.CharField(max_length=100, blank=True)
    info_button_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("title_text"),
            FieldPanel("quote"),
            FieldPanel("main_image"),
        ], heading="Title section"),
        MultiFieldPanel([
            FieldPanel("preview_header"),
            FieldPanel("preview_image_1"),
            FieldPanel("preview_image_2"),
            FieldPanel("preview_image_3"),
            FieldPanel("gallery_button_text"),
            FieldPanel("gallery_button_link"),
        ], heading="Gallery section"),
        MultiFieldPanel([
            FieldPanel("more_info_header"),
            FieldPanel("more_info_text"),
            FieldPanel("more_info_image"),
            FieldPanel("info_button_text"),
            FieldPanel("info_button_link"),
        ], heading="More info section"),

        
    ]



class StoreIndexPage(Page):

    subpage_types = ["app.ProductPage"] 
    def get_context(self, request):
        context = super().get_context(request)
        context["products"] = ProductPage.objects.live().child_of(self)
        return context

class ProductPage(Page):

    parent_page_types = ["app.StoreIndexPage"]
    sku = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    product_image = models.ForeignKey(
                                        "wagtailimages.Image",
                            null=True,
                            blank=True,
                            on_delete=models.SET_NULL,
                            related_name="+",)
    
    description = RichTextField(blank=True, null=True)
    inventory = models.PositiveIntegerField(
    null=True,
    blank=True
    )
    content_panels = Page.content_panels + [
        FieldPanel('sku'),
        FieldPanel('price'),
        FieldPanel('product_image'),
        FieldPanel('description'),
        FieldPanel('inventory'),
        InlinePanel('custom_fields', label = 'Custom fields'),
    ]
    def get_context(self, request):
        context = super().get_context(request)

        fields = []
        for f in self.custom_fields.get_object_list():
            if f.options:
                f.options_array = f.options.split('|')
            else:
                f.options_array = []

            fields.append(f)

        context['custom_fields'] = fields

        return context



class ProductCustomField(Orderable):
    product = ParentalKey(ProductPage, on_delete=models.CASCADE, related_name='custom_fields')
    name = models.CharField(max_length=255)
    options = models.CharField(max_length=500, null=True, blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('options')
    ]