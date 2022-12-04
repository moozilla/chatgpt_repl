# ChatGPT Tool

This tool is a work-in-progress. Most of the code was written by ChatGPT with minimal prompting.

My vision for this tool is to automate some of the back-and-forth with ChatGPT for faster iteration on coding projects. A few ideas:
* allow it to clone open source repos, list files or grep for specific strings, then prompt itself with the results
* allow it to save and execute code (with user approval)
    * automatically fix errors by forwarding error messages and asking it to debug the code

The interface to ChatGPT is provided by this package: https://github.com/acheong08/ChatGPT

## Access Tokens

Currently refreshing access tokens is a manual process. To make this easier I had ChatGPT reverse engineer it's own code and create a bookmarklet to extract an access token from the page. (See `get_access_token_bookmarklet.js`) This removes the need manual extract your token using dev tools.
