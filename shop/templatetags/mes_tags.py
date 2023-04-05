from shop.models import *
from django.db.models import Q
from django import template
register = template.Library()
from urllib.parse import parse_qsl, urljoin, urlparse, urlencode, urlunparse

@register.simple_tag()
def format_string(string: str, *args: str) -> str:
    """
    Adds [args] values to [string]
    String format [string]: "Drew %s dad's %s dead."
    Function call in template: {% format_string string "Dodd's" "dog's" %}
    Result: "Drew Dodd's dad's dog's dead."
    """
    return string % args

@register.filter
def in_category(flag, args):
    # request = get_current_request()
    # Category.objects.get(id=x)

    if flag:
        category, prod_Price_Range, productTypevalue = args.split(' - ')
        category, prod_Price_Range, productTypevalue = eval(category), eval(prod_Price_Range), eval(productTypevalue)

        # if prod_Price_Range:
        #     return Product.objects.filter(category=category)
        # else:
        print(prod_Price_Range)
        return SubProduct.objects.filter(Q(offer_price__range= prod_Price_Range),product__in=Product.objects.filter(category=category).values_list('pk',flat=True), productType= productTypevalue, enabled = True) #Product.objects.filter(Q(offer_price__range= prod_Price_Range),category=category)
    else:
        category = args
        return Category.objects.filter(id=category)


@register.simple_tag
def existsCategory(args):
    # request = get_current_request()
    # Category.objects.get(id=x)

    if args in Product.objects.filter(pk__in = SubProduct.objects.all().values_list('product', flat=True).distinct()).values_list('category', flat=True).distinct():#Product.objects.all().values_list('category', flat=True).distinct():
        return True
    else:
        return False

@register.simple_tag(takes_context=True)
def lessonapp_preserved_filters(context, url, dayofweek):
    print("context", context)
    opts = context.get('productType')
    preserved_filters = context.get('category')
    print('preserved_filters',preserved_filters)
    print('opts',opts)
    parsed_url = list(urlparse(url))
    print('parsed_url',parsed_url)
    parsed_qs = dict(parse_qsl(parsed_url[4]))
    merged_qs = dict()

    if opts and preserved_filters:
        preserved_filters = dict(parse_qsl(preserved_filters))

        match_url = '/%s' % url.partition(get_script_prefix())[2]
        try:
            match = resolve(match_url)
        except Resolver404:
            pass
        else:
            current_url = '%s:%s' % (match.app_name, match.url_name)
            changelist_url = 'admin:%s_%s_changelist' % (opts.app_label, opts.model_name)
            if changelist_url == current_url and '_changelist_filters' in preserved_filters:
                preserved_filters = dict(parse_qsl(preserved_filters['_changelist_filters']))

        # preserved_filters['dayofweek__exact'] = dayofweek
        print(preserved_filters)
        merged_qs.update(preserved_filters)

    print(preserved_filters)
    merged_qs.update(parsed_qs)

    parsed_url[4] = urlencode(merged_qs)
    return urlunparse(parsed_url)
