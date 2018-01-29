
This example shows how to add the Dashbot python sdk to your Alexa skill. I adapted the 
following Amazon example for python alexa skills:

https://developer.amazon.com/alexa-skills-kit/alexa-skill-quick-start-tutorial

The only slightly tricky part is packaging the lamdba function for upload to allow 
the import of extra libraries. I am using the approach of setting up a virtualenv
within my project, installing external libraries into this environment and copying the 
libraries in this environment into the zip file uploaded to Amazon along with my lamdba function code.
This repo contains a file called build.py that automates these tasks (though it may need to be adjusted for your environment).

setup
pip install virtualenv


Step 1 follow the steps in the original tutorial to setup your skill and lambda function.

Step 2 download your lambda function to edit locally
		
		1. In the Amazon console, go to lambda and find your function
		2. At the top choose dropdown menu 'Actions'
		3. select export and download your package

Step 3 unzip the file you downloaded in step 2. Create a folder named 'src' in this unzipped directory and
	copy the lambda_function.py file into it. Copy build.py into the top level of the unzipped directory.
	
Step 4 edit the lambda_function.py file as follows:
	near the top of the file, add:
	
		from dashbot import alexa
		dba = alexa.alexa('DASHBOT_API_KEY)
		
	Edit the lambda_handler function to send the incoming event and response to dashbot as follows:
	
	
# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        response = on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        response =  on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        response =  on_session_ended(event['request'], event['session'])
    
    dba.logIncoming(event)
    dba.logOutgoing(event,response)
    return response
			
	

step 5 run build.py which builds a new virtualenv, installs requests and dashbot into this
	environment, and zips up both the lambda_function file and the installed libraries into a 
	a file called build.zip. 
	
step 6 upload zip file to lambda
		
	

