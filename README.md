# OLXHelper

In need of additional function "Holiday" on polish marketplace olx.pl I created this helper where I would like add more missing functionalities. 

Functions list with short description:
- Holiday: go through all offers adding text to description eg. "I'm on holiday untill xx.xx.xxx", and increase price by specified value to handle extra costs of shipping during holiday or to aware customers of making orders if we i crease price for eg. 1000.

## Setting up Selenium Grid

To run the script with Selenium Grid, follow these steps:

1. **Download and Install Selenium Grid**:
   - Download the Selenium Server jar file from the [official Selenium website](https://www.selenium.dev/downloads/).
   - Start the Selenium Grid Hub:
     ```sh
     java -jar selenium-server-standalone-x.xx.x.jar -role hub
     ```
   - Start the Selenium Grid Node:
     ```sh
     java -jar selenium-server-standalone-x.xx.x.jar -role node -hub http://localhost:4444/grid/register
     ```

2. **Update the `main.py` script**:
   - Ensure the `grid_url` variable is set to the correct URL of your Selenium Grid Hub:
     ```python
     grid_url = "http://localhost:4444/wd/hub"
     ```

3. **Run the Script**:
   - Execute the `main.py` script as usual. The script will now use Selenium Grid to distribute tasks across multiple WebDriver instances.
