css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #2b313e;
    color: white;
    text-align: right;
}

.footer p {
    margin: 0;
    padding: 1rem;
}

a:link {
        color: #64feda;
        background-color: transparent;
        text-decoration: none;
        }

</style>
'''



hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
"""

footer = """
        <div class="footer">
        <p>Made by <a href="https://www.linkedin.com/in/amit-malakar-983175259/" style="color:#64feda;">Amit Malakar</a></p>
        </div>
"""
        