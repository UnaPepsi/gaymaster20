def changelog(version: str):
	if version == "latest":
		version = "2.14.0"
	with open("changelog.txt", "r") as f:
		lines = f.readlines()
		try:
			verIndex = lines.index(f"Version {version}\n")
		except ValueError:
			return "No changelog found"
		changelog = ""
		for line in lines[verIndex::]:
			if line == "End of changelog\n":
				break
			changelog += line
		return changelog
