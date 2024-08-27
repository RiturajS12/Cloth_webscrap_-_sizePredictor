# FashionHub - E-commerce Clothing Store

## Overview

Welcome to FashionHub, an e-commerce platform designed to provide a seamless shopping experience for both men and women. Our platform not only allows users to browse and purchase a wide range of clothing items but also includes a unique feature that helps users determine their clothing size based on their age, weight, and height to ensure the perfect fit.

## Features

- **Browse and Purchase Clothing**: Explore a diverse collection of clothing for both men and women, carefully curated to meet your fashion needs.
  
- **Size Prediction**: Unsure of your size? No worries! Simply input your age, weight, and height, and our intelligent model will predict the best size for you.

- **Web Scraping for Latest Fashion Trends**: The clothing data on FashionHub is dynamically updated through web scraping from Flipkart using BeautifulSoup, ensuring that you have access to the latest trends and styles.

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask for backend services and API creation
- **Machine Learning**: RandomForest model for size prediction
- **Web Scraping**: BeautifulSoup for scraping clothing data from Flipkart
- **Database**: SQLite3 for managing product and user data

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/RiturajS12/Cloth_webscrap_-_sizePredictor.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Cloth_webscrap_-_sizePredictor
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python db.ipynb
   ```

5. Start the development server:
   ```bash
   flask run
   ```

6. Open your browser and navigate to \`http://127.0.0.1:5000\` to explore FashionHub.

## Usage

- **Shopping**: Browse through the available categories, select your desired items, and add them to your cart for purchase.

- **Size Prediction**: On the product page, use the "Predict My Size" option if you’re unsure about your size. Enter your age, weight, and height, and get a personalized size recommendation.

## Contributing

We welcome contributions to improve FashionHub. If you have suggestions for new features or improvements, feel free to open an issue or submit a pull request.

## Acknowledgments

- Special thanks to the developers of BeautifulSoup for making web scraping seamless.
- Thank you to the Flipkart team for providing a platform to source our fashion data.
