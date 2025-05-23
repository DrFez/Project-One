# Part D: Evaluate

## User Acceptance Testing
To make sure my system was actually usable, I asked a few classmates and my teacher to try it out. I gave them a checklist of things to test, like adding products, storing and retrieving items, searching for products, and using the warehouse visualization. I watched how they used the system and took notes on any problems or suggestions they had. Most users were able to complete all the tasks without much help, and the feedback was generally positive. 

## Questionnaire Data

| # | Question | Response Summary |
|---|----------|-----------------|
| 1 | Was the system easy to use? | Most people found the GUI intuitive, though some wanted more descriptive tooltips or an onboarding message. |
| 2 | Did all features work as expected? | Yes, all core features functioned correctly during testing with real data. |
| 3 | Was the warehouse visualization clear? | Yes, users appreciated the 2D grid view and icons representing stock levels. |
| 4 | Were the instructions/documentation sufficient? | Most users said yes, though a few recommended adding a dedicated "Help" tab or user guide. |
| 5 | Was the program responsive and fast? | Yes, operations like adding products or updating quantities were instant and smooth. |
| 6 | Was the system visually appealing? | Majority liked the clean layout and colour coding, though one tester suggested a dark mode option. |
| 7 | Were errors handled clearly? | Yes, most testers appreciated the clear error messages and confirmations, especially on invalid input. |
| 8 | Could you navigate the system without assistance? | Most users could figure things out on their own after 1–2 minutes of use. |
| 9 | Did the CLI feel usable compared to the GUI? | While the GUI was preferred, CLI users said it was functional and useful for quick tasks. |
| 10 | Suggestions for improvement? | Top suggestions included: tooltip help, more advanced filtering, and better visual indicators for nearly full locations. |

I collected this feedback through in-person conversations. I used the results to fix a couple of small bugs and to improve the help text in the GUI.

## Developer Retrospective

Looking back, I’m happy with how the project turned out. Using OOP made the code much easier to manage, and the 2D visualization really helped me (and others) understand the warehouse layout. I did run into some challenges, like making sure the product quantities always matched between the product list and the warehouse locations, but I was able to fix these with validation and extra checks. I also learned a lot about testing and debugging, especially when it came to handling edge cases and user errors.

If I were to keep working on this, I’d probably add a proper help section, maybe a more advanced reporting feature, and possibly a web interface. But overall, I think the project meets all the requirements and is a solid example of OOP in a real-world context.
