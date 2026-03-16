from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet


from django import forms

class HomePage(Page):
    pass

        
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

    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("hero_image"),
        FieldPanel("organization_story"),
        FieldPanel("founder_bio"),
        FieldPanel("mission_statement"),
        FieldPanel("mentalhealth_services")
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
    parent_page_types = ["app.HomePage"] #what ever file is rendering the home page nav bar
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
        FieldPanel("video_url")
    ]


class EventPage(Page): #All the event details.
    
    event_date = models.DateField()
    event_time = models.TimeField()
    event_location = models.CharField(max_length=255)
    event_description = RichTextField()

    ticket_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )

    tickets_available = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("event_date"),
        FieldPanel("event_time"),
        FieldPanel("event_location"),
        FieldPanel("event_description"),
        FieldPanel("ticket_price"),
        FieldPanel("tickets_available"),
    ]
            

class EventIndexPage(Page): #This loops through EventPage and gets all the info to render on the Box Office Page. 
    
    def get_context(self, request):
        context = super().get_context(request)
        context["events"] = EventPage.objects.child_of(self).live().order_by("event_date")
        return context
        

class ProductPage(Page):

    product_image = models.ForeignKey(
    "wagtailimages.Image",
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name="+"
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    description= RichTextField()
    inventory = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("price"),
        FieldPanel("description"),
        FieldPanel("inventory")
    ]


class StoreIndexPage(Page):

    def get_context(self, request):
        context = super().get_context(request)
        context["products"] = ProductPage.objects.live().child_of(self).live()
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
    gallery_button_link = models.URLField(blank=True)

    more_info_header = models.CharField(max_length=100, blank=True)    
    more_info_text = RichTextField(blank=True)
    more_info_image =  models.ForeignKey(
                                "wagtailimages.Image",
                                null=True,
                                blank=True,
                                on_delete=models.SET_NULL,
                                related_name="+",)
    
    info_button_text = models.CharField(max_length=100, blank=True)
    info_button_link = models.URLField(blank=True)
    
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