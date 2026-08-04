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
