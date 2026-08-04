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

    games = (
        data["data"]["Catalog"]["searchStore"]["elements"]
    )

    for game in games:

        promotions = game.get("promotions")

        if not promotions:
            continue

        official.add(game["title"])

    return official

def fetch_catalog(country="US"):
    """
    Fetch one page of Epic catalog.
    """

    payload = {
        "query": BROWSE_QUERY,
        "variables": {
            "category": CATEGORY,
            "count": PAGE_SIZE,
            "country": country,
            "sortBy": "releaseDate",
            "sortDir": "DESC",
            "start": 0,
            "priceRange": None,
        },
    }

    response = requests.post(
        GRAPHQL_URL,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    return (
        response.json()["data"]["Catalog"]
        ["searchStore"]["elements"]
    )

def is_free(game):
    """
    Returns True if the game is temporarily 100% free.
    """

    total = (
        game.get("price", {})
        .get("totalPrice", {})
    )

    original = total.get("originalPrice")

    discount = total.get("discountPrice")

    if original is None or discount is None:
        return False

    return original > 0 and discount == 0

def developer_giveaways(country="US"):
    """
    Return developer giveaways only.
    """

    official = fetch_official_freebies(country)

    catalog = fetch_catalog(country)

    giveaways = []

    for game in catalog:

        if not is_free(game):
            continue

        if game["title"] in official:
            continue

        giveaways.append(game)

    return giveaways
