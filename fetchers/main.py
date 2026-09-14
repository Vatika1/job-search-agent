from fetchers.greenhouse import fetch

SLUGS = ["behavox", "workleap", "lightspeedhq", "lyft", "hopper"]

if __name__ == "__main__":
    total = 0
    for slug in SLUGS:
        for job in fetch(slug):
            print(f"{job['title']} | {job['company']} | {job['location']} | {job['posted_at']} | {job['url']}")
            total += 1
    print(f"\n{total} jobs")