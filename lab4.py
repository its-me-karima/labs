from google_play_scraper import search, app, reviews, Sort
import json
import time

# ==========================================
# SEARCH FOR MENTAL HEALTH AI APPS
# ==========================================

query = "mental health ai"

results = search(
    query,
    lang="en",
    country="us",
    n_hits=20
)

print(f"Found {len(results)} apps")

all_apps = []

# ==========================================
# LOOP THROUGH APPS
# ==========================================

for r in results:

    try:

        app_id = r["appId"]

        print(f"\nExtracting: {app_id}")

        # ==========================================
        # APP DETAILS
        # ==========================================

        details = app(
            app_id,
            lang="en",
            country="us"
        )

        # ==========================================
        # APP REVIEWS
        # ==========================================

        review_data, continuation_token = reviews(
            app_id,
            lang="en",
            country="us",
            sort=Sort.NEWEST,
            count=50
        )

        review_list = []

        for rev in review_data:

            review_list.append({
                "userName": rev.get("userName"),
                "score": rev.get("score"),
                "content": rev.get("content"),
                "at": str(rev.get("at")),
                "replyContent": rev.get("replyContent"),
                "repliedAt": str(rev.get("repliedAt"))
            })

        # ==========================================
        # STORE EVERYTHING
        # ==========================================

        app_data = {
            "appId": details.get("appId"),
            "title": details.get("title"),
            "description": details.get("description"),
            "summary": details.get("summary"),
            "score": details.get("score"),
            "ratings": details.get("ratings"),
            "reviews": details.get("reviews"),
            "installs": details.get("installs"),
            "realInstalls": details.get("realInstalls"),
            "price": details.get("price"),
            "free": details.get("free"),
            "currency": details.get("currency"),
            "developer": details.get("developer"),
            "genre": details.get("genre"),
            "genreId": details.get("genreId"),
            "contentRating": details.get("contentRating"),
            "url": details.get("url"),
            "reviews_data": review_list
        }

        all_apps.append(app_data)

        time.sleep(2)

    except Exception as e:
        print("Error:", e)

# ==========================================
# SAVE TO JSON
# ==========================================

with open("mental_health_ai_apps.json", "w", encoding="utf-8") as f:
    json.dump(all_apps, f, indent=4, ensure_ascii=False)

print("\nJSON file created successfully")
print(f"Total apps extracted: {len(all_apps)}")