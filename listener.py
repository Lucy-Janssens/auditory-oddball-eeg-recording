from pylsl import StreamInlet, resolve_streams
import time

def receive_data(selected_stream):
    inlet = StreamInlet(selected_stream)
    print("Listening for data...")
    try:
        while True:
            sample, timestamp = inlet.pull_sample()
            print(f"Received sample: {sample} at timestamp: {timestamp}")
    except KeyboardInterrupt:
        print("Stopping...")

def main():
    while True:
        print("Looking for LSL streams...")
        streams = resolve_streams()

        # Print information about each stream
        for idx, stream in enumerate(streams):
            print(f"Stream {idx + 1}:")
            print(f"  Name: {stream.name()}")
            print(f"  Type: {stream.type()}")
            print(f"  Channel Count: {stream.channel_count()}")
            print(f"  Sampling Rate: {stream.nominal_srate()} Hz")
            print(f"  Source ID: {stream.source_id()}")
            print(f"  Stream ID: {stream.uid()}")
            print()

        if streams:
            selection = input("Enter the number of the stream you want to connect to (or 'q' to quit): ")
            if selection.lower() == 'q':
                break
            try:
                selected_index = int(selection) - 1
                if 0 <= selected_index < len(streams):
                    selected_stream = streams[selected_index]
                    receive_data(selected_stream)
                else:
                    print("Invalid stream number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid stream number.")
        else:
            print("No streams found.")

if __name__ == "__main__":
    main()
