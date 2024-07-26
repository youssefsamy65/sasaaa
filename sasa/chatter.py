import roslibpy

def republish_message(message):
    # Publish the message to the new topic
    publisher.publish(message)

def main():
    # Initialize the ROS client
    client = roslibpy.Ros(host='localhost', port=9090)
    
    # Connect to ROS
    client.run()
    
    # Create a subscriber for the /republish_chatter topic
    subscriber = roslibpy.Topic(client, '/republish_chatter', 'std_msgs/String')
    
    # Create a publisher for the /chatter topic
    global publisher
    publisher = roslibpy.Topic(client, '/chatter', 'std_msgs/String')
    
    # Define the callback function for the subscriber
    def callback(message):
        print(f"Received message: {message['data']}")
        republish_message(message)
    
    # Subscribe to the /republish_chatter topic
    subscriber.subscribe(callback)
    
    # Keep the program running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        # Unsubscribe and close the client on exit
        subscriber.unsubscribe()
        publisher.unadvertise()
        client.terminate()

if __name__ == "__main__":
    main()

