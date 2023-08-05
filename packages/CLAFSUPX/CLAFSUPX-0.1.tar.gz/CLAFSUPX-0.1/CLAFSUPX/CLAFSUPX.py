import requests
def sup(id):
	ch = "CC22M"
	join = requests.get(f"https://api.telegram.org/bot6088451625:AAFs598Ov63pyIXPM8Ak9mEz_iLtrnw9u7M/getChatMember?chat_id=@{ch}&user_id={id}").text
	if '"status":"left"' in join:
		return 'FALSE'
	else:
		return "TRUE"