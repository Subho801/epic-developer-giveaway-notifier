import requests

GRAPHQL_URL = "https://store.epicgames.com/graphql"

OFFICIAL_API_URL = (
    "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
)

CATEGORY = (
    "games/edition/base|bundles/games|editors|software/edition/base"
)

PAGE_SIZE = 40


BROWSE_QUERY = """
query searchStoreQuery(
  $category:String,
  $count:Int,
  $country:String!,
  $sortBy:String,
  $sortDir:String,
  $start:Int,
  $priceRange:String
){
  Catalog{
    searchStore(
      category:$category,
      count:$count,
      country:$country,
      sortBy:$sortBy,
      sortDir:$sortDir,
      start:$start,
      priceRange:$priceRange
    ){
      paging{
        count
        total
      }

      elements{
        id
        title
        productSlug
        urlSlug

        offerMappings{
          pageSlug
          pageType
        }

        developerDisplayName
        publisherDisplayName

        seller{
          name
        }

        keyImages{
          type
          url
        }

        effectiveDate
        expiryDate

        price(country:$country){
          totalPrice{
            originalPrice
            discountPrice
            currencyCode
            fmtPrice{
              originalPrice
              discountPrice
            }
          }
        }

        promotions{
          promotionalOffers{
            promotionalOffers{
              startDate
              endDate
            }
          }
        }
      }
    }
  }
}
"""
def fetch_official_freebies(country="US"):
    """
    Fetch Epic's official weekly free games.
    """

    params = {
        "locale": "en-US",
        "country": country,
        "allowCountries": country,
    }

    response = requests.get(
        OFFICIAL_API_URL,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    official = set()

    elements = (
        data["data"]["Catalog"]["searchStore"]["elements"]
    )

    for game in elements:

        if not game.get("promotions"):
            continue

        title = game.get("title")
        slug = game.get("productSlug") or game.get("urlSlug")

        if title:
            official.add(title)

        if slug:
            official.add(slug)

    return official
def fetch_catalog_page(country="US", start=0):
    """
    Fetch a single page from the Epic catalog.
    """

    payload = {
        "query": BROWSE_QUERY,
        "variables": {
            "category": CATEGORY,
            "count": PAGE_SIZE,
            "country": country,
            "sortBy": "releaseDate",
            "sortDir": "DESC",
            "start": start,
            "priceRange": None,
        },
    }

    response = requests.post(
        GRAPHQL_URL,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    search = (
        response.json()["data"]["Catalog"]["searchStore"]
    )

    return (
        search["elements"],
        search["paging"]["total"]
    )

def fetch_all_catalog(country="US"):
    """
    Fetch every page of the Epic catalog.
    """

    games = []

    start = 0
    total = None

    while True:

        elements, total_results = fetch_catalog_page(
            country,
            start,
        )

        games.extend(elements)

        if total is None:
            total = total_results

        start += PAGE_SIZE

        if start >= total:
            break

    return games

def is_free(game):
    """
    Return True if the game is currently 100% off.
    """

    price = game.get("price")

    if not price:
        return False

    total = price.get("totalPrice")

    if not total:
        return False

    original = total.get("originalPrice")
    discount = total.get("discountPrice")

    if original is None or discount is None:
        return False

    return original > 0 and discount == 0

def developer_giveaways(country="US"):
    """
    Return only developer giveaways.
    """

    official = fetch_official_freebies(country)

    catalog = fetch_all_catalog(country)

    giveaways = []

    for game in catalog:

        if not is_free(game):
            continue

        title = game.get("title")
        slug = game.get("productSlug") or game.get("urlSlug")

        if title in official:
            continue

        if slug in official:
            continue

        giveaways.append(game)

    return giveaways

def get_developer(game):
    return (
        game.get("developerDisplayName")
        or game.get("publisherDisplayName")
        or (game.get("seller") or {}).get("name")
        or "Unknown"
    )


def get_publisher(game):
    return (
        game.get("publisherDisplayName")
        or (game.get("seller") or {}).get("name")
        or "Unknown"
    )


def get_original_price(game):
    total = (game.get("price") or {}).get("totalPrice") or {}

    fmt = total.get("fmtPrice") or {}
    if fmt.get("originalPrice"):
        return fmt["originalPrice"]

    value = total.get("originalPrice")
    currency = total.get("currencyCode", "")

    if value is None:
        return "Unknown"

    if currency == "USD":
        return f"${value / 100:.2f}"

    return f"{value / 100:.2f} {currency}"


def get_end_date(game):
    promos = (game.get("promotions") or {}).get("promotionalOffers") or []

    if promos:
        offers = promos[0].get("promotionalOffers") or []
        if offers:
            return offers[0].get("endDate")

    return game.get("expiryDate")
