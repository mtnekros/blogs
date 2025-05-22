from collections.abc import Callable

from rapidfuzz import fuzz, process

with open("C:/Users/mtnek/projects/clara/aijobs-python/app/config/cities.csv", encoding="utf-8-sig") as csv:
    city_col_index = 1
    cities = [line.split(",")[city_col_index] for line in csv]

def run_test(scorer: Callable, threshold: int=50) -> None:
    """Run tests with given fuzzy algorithm."""
    cities_from_llm = [
        "יבנה",
        "אשדוד",
        "אשדוד",
        "רמלה",
        "אשקלון",
        "לוד",
        "חיפה",
        "רחובות",
        "גבעת שמואל",
        "רחובות",
        "כרמיאל",
        "כפר בילו",
        "מודיעין מכבים רעות",
        "מודיעין",
        "מודיעין",
        "מודיעין",
    ]

    n_exact_matches = 0
    n_fuzzy_matches = 0
    for residence in cities_from_llm:
        best_match = process.extractOne(residence, choices=cities, scorer=scorer, score_cutoff=threshold)

        best_match_value = best_match[0] if best_match else ""

        exact_match_found = residence in cities
        fuzzy_match_found = bool(best_match)

        print(f"LLM: { residence }\tFuzzyFind: '{best_match_value}'\tExactMatch: {exact_match_found}")
        if exact_match_found:
            n_exact_matches += 1
        if fuzzy_match_found:
            n_fuzzy_matches += 1

    print(f"\nTotal Resdence: {len(cities_from_llm)}, Exact Match: {n_exact_matches}, Fuzzy Matches: {n_fuzzy_matches}")


if __name__ == "__main__":
    score_threshold = 85
    run_test(fuzz.ratio, score_threshold)
    run_test(fuzz.WRatio, score_threshold)
    run_test(fuzz.token_sort_ratio, score_threshold)
    run_test(fuzz.token_set_ratio, score_threshold)
    run_test(fuzz.partial_token_ratio, score_threshold)
