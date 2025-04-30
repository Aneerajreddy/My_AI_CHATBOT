# Local Passive Assistant - By Neeraj

This is a local, passive assistant that monitors screen and clipboard activity, provides text extraction from images, and allows chat interaction. It’s designed to work without sending data online, ensuring complete privacy for the user.

## Features

- **Screen Capture**: Captures screenshots every 10 seconds for OCR (text recognition) and activity monitoring.
- **OCR (Optical Character Recognition)**: Extracts text from captured images.
- **Clipboard Monitoring**: Monitors clipboard content.
- **Chat Interaction**: Interact with the assistant through a chat interface, powered by the Ollama model.
- **Dark/Light Theme**: Toggle between light and dark themes for the UI.
- **Logs**: View logs of captured events, including screen text, clipboard contents, and active window titles.
- **Desktop Shortcut**: Automatically creates a shortcut on the user's desktop for easy access.
- **Local-Only Data**: All data captured by the assistant is stored locally on the user's computer and is never sent online.

## Requirements

- **Operating System**: Windows 7 or higher.
- **Permissions**: 
  - **Administrator**: To install the app and create the desktop shortcut.
  - **Screen Capture Permission**: Must grant permission for the app to capture screen data.
- **Disk Space**: At least 50MB of free storage for logs and screenshots.
- **.NET Framework**: Required for Windows versions prior to Windows 10.

## Installation

1. **Download the Executable**:
   - Download the latest release `.exe` file from the [Releases](https://github.com/yourusername/your-repository/releases) section.

2. **Run the Executable**:
   - Double-click the `.exe` file to run the application. The application will start without requiring Python or additional dependencies to be installed.

3. **Grant Permissions**:
   - On the first run, you'll be prompted to grant screen capture permission. Click on **Grant Permission** to allow the app to capture screen data.

4. **Create Desktop Shortcut**:
   - The application will create a shortcut on the desktop automatically. You can launch the app from the shortcut.

## Usage

1. **Grant Screen Capture Permission**: Click **Grant Permission** to allow the app to access screen and clipboard data.
2. **Start Monitoring**: Click **Start Monitoring** to begin screen and clipboard monitoring. The app will capture screenshots and monitor activity every 10 seconds.
3. **Chat Interface**: Type in the chatbox to interact with the assistant. It will respond based on the screen and clipboard activity.
4. **Toggle Theme**: Switch between light and dark themes using the **Toggle Theme** button.
5. **View Logs**: You can view logs of captured data by clicking **View Logs**.
6. **Help/FAQ**: Access frequently asked questions via the **Help / FAQ** button.

## How It Works

- **Screen Capture**: The app captures screenshots every 10 seconds using the `screen_capture` module.
- **OCR**: Extracts text from screenshots using `ocr_reader` and provides insights into the screen content.
- **Clipboard Monitoring**: Continuously monitors the clipboard using the `clipboard_monitor` module.
- **Bot Response**: The assistant uses the captured data to generate responses using the Ollama model, which processes the data and provides relevant answers.
- **Logging**: All captured events, including active window titles, clipboard content, and screen text, are logged for review.

## FAQ

- **What does this app do?**
  - It captures your screen, extracts text from images, and monitors clipboard activity locally without transmitting any data online.
  
- **Is my data safe?**
  - Yes, everything stays on your computer. No data is sent online.

- **How often does it capture?**
  - By default, the app captures your screen every 10 seconds.

- **Can I select an image manually?**
  - Yes, use the "📷 Attach Photo" button to manually select an image for text extraction.

## Troubleshooting

- **The app doesn't start**: Make sure your system has the necessary .NET Framework installed. If the issue persists, ensure that the antivirus is not blocking the executable.
- **No desktop shortcut created**: Right-click on the `.exe` file and select "Create shortcut" to manually create a desktop shortcut.
- **OCR not working**: Ensure the app has screen capture permissions, and check if the app is running with administrator rights.

## Contributing

Feel free to fork the repository, create pull requests, and report any bugs or issues. Contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact: [your.email@example.com](mailto:your.email@example.com)

