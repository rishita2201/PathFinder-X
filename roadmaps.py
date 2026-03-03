def generate_roadmap(missing_skills):
    roadmap = []
    for skill in missing_skills:
        roadmap.append(f"Complete online course on {skill}")
        roadmap.append(f"Build a mini project using {skill}")
        roadmap.append(f"Get certification in {skill}")
    return roadmap