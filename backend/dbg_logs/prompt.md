Your job is to create jira tickets by calling jira_ticket_creator.create_ticket. Your output will be executed using eval, so only output valid python code (one call for each item on the to-do-list). Tasks should be concrete items with a clear definition of done and a concise description of what needs to be done.Here's the context: ```json {'project_key': <class 'str'>, 'summary': <class 'str'>, 'description': <class 'str'>, 'issue_type': <class 'str'>, 'assignee': typing.Optional[str], 'labels': typing.Optional[list], 'return': typing.Dict}```and the following documentation: 
        Create a new Jira ticket

        Args:
            project_key: The project key where the ticket should be created
            summary: Title of the ticket
            description: Detailed description of the ticket
            issue_type: Type of issue (e.g., 'Task', 'Bug', 'Story')
            assignee: Email of the person to assign the ticket to
            labels: List of labels to add to the ticket

        Returns:
            Dict containing the response from Jira API
         using the summary: **Meeting Log Summary**

The meeting discusses the team's progress and future plans for the app. The main topics covered are:

* Authentication upgrades, including adding Google, Facebook, and Apple Sign-in (Sprint 2)
* Enhancing user expectations by allowing multiple profile photos and creating a gallery feature (Sprint 3)
* Content moderation and automated filters for image uploads (Sprint 4)
* Notifications, including push notifications for new messages or matches (Sprint 3)
* Matching algorithm improvements, including integrating advanced filters and user-set preferences (Sprints 5-6)
* Discovery/explore features to browse profiles beyond matches (later sprints)
* Security measures, such as encryption and data privacy tools, to be implemented gradually (Sprints 4-6)

**Open Tasks**

Here are the open tasks identified in the meeting:

* Add Google and Facebook authentication for Sprint 2
* Implement multiple profile photos and gallery feature for Sprint 3
* Develop content moderation and automated filters for image uploads for Sprint 4
* Set up notification backend for push notifications and email notifications (Sprint 3)
* Improve matching algorithm to consider advanced filters and user-set preferences (Sprints 5-6)
* Create discovery/explore features to browse profiles beyond matches (later sprints)
* Implement security measures, including encryption and data privacy tools, gradually (Sprints 4-6). The project_key is SCRUM. Use named parameters.Put an empty string if you're unsure about the assignee or the due date.