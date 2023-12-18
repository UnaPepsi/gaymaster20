def changelog(version: str):
  if version == "latest":
    version = "2.12.0"
  with open("changelog.txt", "r") as f:
    lines = f.readlines()
    verIndex = lines.index(f"Version {version}\n")
    changelog = ""
    for line in lines[verIndex::]:
      if line == "End of changelog\n":
        break
      changelog += line
    return changelog if changelog != "" else "No changelog found"
