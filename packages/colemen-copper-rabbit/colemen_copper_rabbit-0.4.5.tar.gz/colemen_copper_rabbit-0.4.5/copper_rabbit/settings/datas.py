



valid_status_codes = ["100","101","102","103","200","201","202","203","204","205","206","207","208","226","300","301","302","303","304","305","306","307","308","400","401","402","403","404","405","406","407","408","409","410","411","412","413","414","415","416","417","418","421","422","423","424","425","426","428","429","431","451","500","501","502","503","504","505","506","507","508","510","511"]
'''A list of valid http status codes'''
valid_crud_types = ["create","read","update","delete"]
valid_request_methods = ["connect","delete","get","head","options","patch","post","put","trace"]


validation_errors_public_responses = [
    "(Correct|Fix) the (errors|problems|issues)( and try again.)?",
    # "Correct the problems and try again.",
    # "Fix the issues and try again.",
    # "Fix the problems and try again.",
    "Lets try that (again|another time|once more).",
]
'''A list of public responses that can be used when a validation error occurs'''

successful_get_action_responses = [
    "Here is the (stuff|thing)(\.|!)",
    "I got your (stuff|thing)(\.|!)",
    "Found (it|'em)(\.|!)",
]
'''A list of public responses that can be used when an action is successfully performed'''

successful_create_action_responses = [
    "Saved(\.|!)"
]
'''A list of public responses that can be used when a create action is successfully performed'''
successful_update_action_responses = [
    "(Saved|Updated)(\.|!)"
]
'''A list of public responses that can be used when an update action is successfully performed'''

no_values_found_responses=[
    "Nothing( to see)? here(\.|!)",
    "There is nothing (there|here)(\.|!)",
    "Just emptiness",
    "(Didn't|Couldn't) find anything (brosferatu|brostradamus|bruh|bro)(\.|!)",
]
'''A list of public responses that can be used when an action is successfully performed but nothing is found.'''


