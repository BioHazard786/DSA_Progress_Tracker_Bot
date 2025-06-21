# DSA Progress Tracker Bot 📊

A powerful Telegram bot designed to help you track your Data Structures and Algorithms (DSA) progress across both **LeetCode** and **Striver's Sheet**. Monitor your coding journey with detailed statistics, progress bars, and motivational insights!

## 🚀 Features

### 📈 LeetCode Integration

- Track your LeetCode problem-solving progress
- View detailed statistics by difficulty (Easy, Medium, Hard)
- Visual progress bars for better understanding
- Real-time data fetching from LeetCode's GraphQL API

### 📚 Striver Sheet Integration

- Monitor your progress on Striver's famous Sheets
- Topic-wise breakdown of solved problems
- Comprehensive statistics across all DSA topics

### 🎯 Interactive Dashboard

- Beautiful inline keyboard navigation
- Real-time progress updates
- User-friendly interface with emojis and formatting
- Motivational messages based on your progress

### 🔧 Bot Management

- System statistics monitoring
- Uptime tracking
- Resource usage information (CPU, RAM, Disk)
- Logging capabilities

## 🛠️ Tech Stack

- **Python 3.10+**
- **Pyrogram** - Modern Telegram Bot API framework
- **MongoDB** - Database for user data storage
- **Docker** - Containerization for easy deployment
- **httpx** - Async HTTP client for API requests
- **Motor** - Async MongoDB driver

## 📋 Prerequisites

Before running the bot, ensure you have:

1. **Telegram Bot Token** - Get it from [@BotFather](https://t.me/BotFather)
2. **Telegram API Credentials** - Get from [my.telegram.org](https://my.telegram.org)
3. **MongoDB Database** - MongoDB Atlas or local instance
4. **Python 3.10+** installed
5. **Docker** (optional, for containerized deployment)

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/BioHazard786/DSA_Progress_Tracker_Bot.git
cd "DSA Progress Tracker Bot"
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `config.env` file in the root directory:

```env
# Telegram Bot Configuration
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token

# MongoDB Configuration
MONGO_URL=your_mongodb_connection_string
MONGO_DB_NAME=dsa_bot

# Optional
OWNER_ID=your_telegram_user_id
SESSION_NAME=DSA-Progress-Tracker-Bot
```

### 4. Run the Bot

#### Method 1: Direct Python Execution

```bash
python -m Bot
```

#### Method 2: Docker Compose (Recommended)

```bash
docker-compose up -d
```

## 🎮 Bot Commands

| Command                         | Description                                           |
| ------------------------------- | ----------------------------------------------------- |
| `/start`                        | Start the bot and get a welcome message               |
| `/add_leetcode_user <username>` | Add your LeetCode username to track progress          |
| `/add_striver_user <username>`  | Add your Striver profile to track sheet progress      |
| `/info`                         | View your progress dashboard with interactive buttons |
| `/stats`                        | Get bot system statistics and uptime information      |
| `/logs`                         | View recent bot logs (owner only)                     |

## 📱 How to Use

### 1. **Getting Started**

- Start the bot with `/start`
- Add your usernames using the respective commands

### 2. **Adding LeetCode Profile**

```
/add_leetcode_user your_leetcode_username
```

- Bot will fetch and verify your profile
- Confirm to add it to the database

### 3. **Adding Striver Profile**

```
/add_striver_user your_striver_username
```

- Bot will verify your Striver profile
- Confirm to save your data

### 4. **Viewing Progress**

```
/info
```

- Interactive dashboard with buttons
- Choose between LeetCode or Striver progress
- Navigate easily with back buttons

## 🏗️ Project Structure

```
Striver Sheet Bot/
├── Bot/
│   ├── __init__.py          # Bot initialization and plugin loading
│   ├── __main__.py          # Main entry point
│   ├── config.py            # Configuration management
│   ├── constants.py         # Bot constants and topic mappings
│   ├── logging.py           # Logging configuration
│   ├── Database/
│   │   └── mongo_db.py      # MongoDB operations
│   ├── Helpers/
│   │   ├── filters.py       # Custom filters for commands
│   │   ├── leetcode_utils.py # LeetCode API utilities
│   │   └── utils.py         # General utility functions
│   └── Plugins/
│       ├── add_leetcode_user.py    # LeetCode user management
│       ├── add_striver_user.py     # Striver user management
│       ├── info.py                 # Main dashboard
│       ├── leetcode_info.py        # LeetCode progress display
│       ├── striver_info.py         # Striver progress display
│       ├── start.py                # Start command
│       ├── stats.py                # System statistics
│       └── logs.py                 # Log viewing
├── config.env               # Environment variables
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
└── README.md              # Project documentation
```

## 📊 Features in Detail

### LeetCode Progress Tracking

- **Overall Statistics**: Total problems solved with percentage
- **Difficulty Breakdown**: Easy, Medium, Hard problem counts
- **Visual Progress Bars**: ASCII progress indicators
- **Motivational Messages**: Dynamic messages based on progress level

### Striver Sheet Progress

- **Topic-wise Statistics**: Problems solved per DSA topic
- **Comprehensive Coverage**: All major DSA topics included
- **Sorted Display**: Topics sorted by problems solved
- **Real-time Updates**: Live data from Striver's backend

### Interactive Navigation

- **Inline Keyboards**: Easy navigation between different views
- **User Verification**: Ensures only the command initiator can interact
- **Clean Interface**: Delete and back buttons for better UX

## 🔒 Security Features

- **User Verification**: Callback queries are verified against the initiating user
- **Environment Variables**: Sensitive data stored securely
- **Error Handling**: Graceful error handling for API failures
- **Input Validation**: Username validation and sanitization

## 🚀 Deployment Options

### Local Development

```bash
python -m Bot
```

### Docker Deployment

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Production Deployment

- Use environment variables for configuration
- Set up proper logging and monitoring
- Configure automatic restarts
- Use a reverse proxy if needed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

1. **Bot not responding**

   - Check if the bot token is correct
   - Verify internet connectivity
   - Check Docker container status

2. **Database connection errors**

   - Verify MongoDB URL in config.env
   - Check if MongoDB service is running
   - Validate database permissions

3. **API errors**
   - LeetCode API might be rate-limited
   - Striver API might be temporarily unavailable
   - Check username spelling and existence

### Getting Help

- Create an issue on GitHub for bugs
- Check logs using `/logs` command (if you're the owner)
- Verify all environment variables are set correctly

## 📞 Support

If you encounter any issues or have questions:

- Open an issue on GitHub
- Check the troubleshooting section
- Review the logs for error messages

---

**Happy Coding! 🎉**

Track your DSA journey efficiently and stay motivated with detailed progress insights!
