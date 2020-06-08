text_template_str = open('rangers_email.txt').read()
text_template = Template(text_template_str)
html_template_str = open('rangers_email.html').read()
html_template = Template(html_template_str)
