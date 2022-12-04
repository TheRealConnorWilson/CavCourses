"""
REFERENCES

Referenced Megan Kuo's django tutorial project 

Used to figure out how to use forms and the HTML for it
Title: authorForm
Author: MDN contributors, Mozilla Contributors
Date: 9.22.22
URL: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms#generic_editing_views
Software License: public domain
Helpful resources from a TA:
Title: manage_authors(), authorForm, ArtileForm()
Date: 9.22.22
URL: https://docs.djangoproject.com/en/4.1/topics/forms/modelforms/
Title: ContactForm()
Author: Vitor Freitas
Date: 9.22.22
URL: https://simpleisbetterthancomplex.com/article/2017/08/19/how-to-render-django-form-manually.html
Software License: Attribution-NonCommercial-ShareAlike 3.0 Unported (CC BY-NC-SA 3.0)
Title: views.py, template.html
Author: W3Schools contributors
Date: 9.22.22
URL: https://www.w3schools.com/django/django_template_variables.php
other tips: 
combine two forms, deal with input elsewhere
model for deepthought, deep thought form class (creating new models from form, specific classes to make it easier for us)
class 
artile form, 
second page
 views.py, form
DO NOT DO contact form class
author form
don't pass, save() to database
also gets called for get request, generates new form
"""

import datetime
from email.charset import Charset

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Account

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class UserAccountForm(UserCreationForm):
    username = forms.CharField()
    email = forms.EmailField()
    major = forms.CharField()
    year = forms.CharField()
    
    class Meta:
        model = Account
        fields = ['username', 'major', 'year']
        

        # def clean_email_address(self):
        #     data = self.cleaned_data['email_address']

        #     # Check if a title is not blank.
        #     if len(data) == 0:
        #         raise ValidationError(_('No text in submission!'))

        #     # # Check if a date is in the allowed range (+4 weeks from today).
        #     # if data > datetime.date.today() + datetime.timedelta(weeks=4):
        #     #     raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        #     # # Remember to always return the cleaned data.
        #     # cleaned_data = super(ContactForm, self).clean()
            
        #     return data

class SearchForm(forms.Form):
    searched_dept = forms.CharField(label='', max_length=4)


dept_choices = [
    ("", "Select a department"),
    ("ACCT", "ACCT - Accounting"),
    ("AIRS", "AIRS - Air Science"),
    ("ALAR", "ALAR - Architecture and Landscape Architecture"),
    ("AM", "AM - Applied Mechanics"),
    ("AMST", "AMST- American Studies"),
    ("ANTH", "ANTH - Anthropology"),
    ("APMA", "APMA - Applied Mathematics"),
    ("ARAB", "ARAB - Arabic"),
    ("ARAD", "ARAD - Arts Administration"),
    ("ARAH", "ARAH - History of Art and Architecture"),
    ("ARCH", "ARCH - Architecture"),
    ("ARCY", "ARCY - Archaeology"),
    ("ARH", "ARH - Architectural History"),
    ("ARTH", "ARTH - History of Art"),
    ("ARTR", "ARTR - Arabic in Translation"),
    ("ARTS", "ARTS - Studio Art"),
    ("ASL", "ASL - American Sign Language"),
    ("ASTR", "ASTR - Astronomy"),
    ("BIMS", "BIMS - Biomedical Sciences"),
    ("BIOC", "BIOC - Biochemistry"),
    ("BIOL", "BIOL - Biology"),
    ("BIOP", "BIOP - Biophysics"),
    ("BME", "BME - Biomedical Engineering"),
    ("BUS", "BUS - Business"),
    ("CASS", "CASS - College Art Scholars Seminar"),
    ("CE", "CE - Civil Engineering"),
    ("CELL", "CELL - Cell Biology"),
    ("CHE", "CHE - Chemical Engineering"),
    ("CHEM", "CHEM - Chemistry"),
    ("CHIN", "CHIN - Chinese"),
    ("CHTR", "CHTR - Chinese in Translation"),
    ("CLAS", "CLAS - Classics"),
    ("COGS", "COGS - Cognitive Science"),
    ("COLA", "COLA"),
    ("COMM", "COMM - Commerce"),
    ("CONC", "CONC"),
    ("CPE", "CPE - Computer Engineering"),
    ("CREO", "CREO - Creole"),
    ("CS", "CS - Computer Science"),
    ("DANC", "DANC - Dance"),
    ("DEM", "DEM"),
    ("DH", "DH - Digital Humanities"),
    ("DRAM", "DRAM - Drama"),
    ("DS", "DS - Data Science"),
    ("EALC", "EALC - East Asian Languages, Literatures, and Cultures"),
    ("EAST", "EAST - East Asian Studies"),
    ("ECE", "ECE - Electrical and Computer Engineering"),
    ("ECON", "ECON - Economics"),
    ("EDHS", "EDHS - Education-Human Services"),
    ("EDIS", "EDIS - Education-Curriculum, Instruction, & Special Ed"),
    ("EDLF", "EDLF - Education-Leadership, Foundations, and Policy"),
    ("EDNC", "EDNC - Education Non-Credit"),
    ("EGMT", "EGMT - Engagement"),
    ("ELA", "ELA"),
    ("ENCW", "ENCW - Creative Writing"),
    ("ENGL", "ENGL - English-Literature"),
    ("ENGR", "ENGR - Engineering"),
    ("ENTP", "ENTP - Entrepreneurship"),
    ("ENWR", "ENWR - Writing and Rhetoric"),
    ("ESL", "ESL - English as a Second Language"),
    ("ETP", "ETP - Enviromental Thought and Practice"),
    ("EURS", "EURS - European Studies"),
    ("EVAT", "EVAT - Environmental Sciences-Atmospheric Sciences"),
    ("EVEC", "EVEC - Environmental Sciences-Ecology"),
    ("EVGE", "EVGE - Environmental Sciences-Geosciences"),
    ("EVHY", "EVHY"),
    ("EVSC", "EVSC - Environmental Sciences"),
    ("FREN", "FREN - French"),
    ("GBAC", "GBAC - Grad Business Analytics Comm."),
    ("GBUS", "GBUS - Graduate Business"),
    ("GCCS", "GCCS"),
    ("GCNL", "GCNL - Clinical Nurse Leader"),
    ("GCOM", "GCOM - Graduate Commerce"),
    ("GDS", "GDS - Global Development Studies"),
    ("GERM", "GERM - German"),
    ("GETR", "GETR - German in Translation"),
    ("GHSS", "GHSS - Grad Humanities & Social Sci"),
    ("GNUR", "GNUR - Graduate Nursing"),
    ("GREE", "GREE - Greek"),
    ("GSAS", "GSAS"),
    ("GSCI", "GSCI"),
    ("GSGS", "GSGS - Global Studies-Global Studies"),
    ("GSMS", "GSMS - GS-Middle East and South Asia"),
    ("GSSJ", "GSSJ - Global Studies-Security and Justice"),
    ("GSVS", "GSVS - Global Studies-Environments and Sustainability"),
    ("HBIO", "HBIO - Human Biology"),
    ("HEBR", "HEBR - Hebrew"),
    ("HHE", "HHE"),
    ("HIAF", "HIAF - History-African History"),
    ("HIEA", "HIEA - History-East Asian History"),
    ("HIEU", "HIEU - History-European History"),
    ("HILA", "HILA - History-Latin American History"),
    ("HIME", "HIME - History-Middle Eastern History"),
    ("HIND", "HIND - Hindi"),
    ("HISA", "HISA - History-South Asian History"),
    ("HIST", "HIST - History-General History"),
    ("HIUS", "HIUS - History-United States History"),
    ("HR", "HR - Human Resources"),
    ("HSCI", "HSCI - College Science Scholars Seminar"),
    ("IMP", "IMP - Interdisciplinary Thesis"),
    ("INST", "INST - Interdisciplinary Studies"),
    ("ISBU", "ISBU - Interdisciplinary Studies-Business"),
    ("ISHU", "ISHU - Interdisiplinary Studies-Humanities"),
    ("ISHU", "ISHU - Interdisciplinary Studies-Individualized Other"),
    ("ISLS", "ISLS - Interdisciplinary Studies-Liberal Studies Seminar"),
    ("ISSS", "ISSS - Interdisciplinary Studies-Social Sciences"),
    ("IT", "IT - Informational Technology"),
    ("ITAL", "ITAL - Italian"),
    ("ITTR", "ITTR - Italian in Translation"),
    ("JAPN", "JAPN - Japanese"),
    ("JPTR", "JPTR - Japanese in Translation"),
    ("KICH", "KICH - Maya K'iche"),
    ("KINE", "KINE - Kinesiology"),
    ("KLPA", "KLPA - Lifetime Physical Activity"),
    ("KOR", "KOR - Korean"),
    ("LAR", "LAR - Landscape Architecture"),
    ("LASE", "LASE - Liberal Arts Seminar"),
    ("LAST", "LAST - Latin American Studies"),
    ("LATI", "LATI - Latin"),
    ("LAW", "LAW - Law"),
    ("LING", "LING - Linguistics"),
    ("LNGS", "LNGS - General Linguistics"),
    ("LPPA", "LPPA - Leadership and Public Policy - Evaluation and Analysis"),
    ("LPPL", "LPPL - Leadership and Public Policy - Leadership"),
    ("LPPP", "LPPP - Leadership and Public Policy - Policy"),
    ("LPPS", "LPPS - Leadership and Public Policy - Substantive"),
    ("MAE", "MAE - Mechanical & Aerospace Engineering"),
    ("MATH", "MATH - Mathematics"),
    ("MDST", "MDST - Media Studies"),
    ("MED", "MED - Medicine"),
    ("MESA", "MESA - Middle Eastern & South Asian Languages & Cultures"),
    ("MICR", "MICR - Microbiology"),
    ("MISC", "MISC - Military Science"),
    ("MSE", "MSE - Materials Science and Engineering"),
    ("MSP", "MSP - Medieval Studies"),
    ("MUBD", "MUBD - Music-Marching Band"),
    ("MUEN", "MUEN - Music-Ensembles"),
    ("MUPF", "MUPF - Music-Private Performance Instruction"),
    ("MUSI", "MUSI - Music"),
    ("NASC", "NASC - Naval Science"),
    ("NCPR", "NCPR - Non-Credit Professional Review"),
    ("NESC", "NESC - Neuroscience"),
    ("NUCO", "NUCO - Nursing Core"),
    ("NUIP", "NUIP - Nursing Interprofessional"),
    ("NURS", "NURS - Nursing"),
    ("PATH", "PATH - Pathology"),
    ("PC", "PC - Procurement and Contracts Management"),
    ("PERS", "PERS - Persian"),
    ("PETR", "PETR - Persian in Translation"),
    ("PHAR", "PHAR - Pharmacology"),
    ("PHIL", "PHIL - Philosophy"),
    ("PHS", "PHS - Public Health Sciences"),
    ("PHY", "PHY - Physiology"),
    ("PHYS", "PHYS - Physics"),
    ("PLAC", "PLAC - Planning Application"),
    ("PLAD", "PLAD - Politics-Departmental Seminar"),
    ("PLAN", "PLAN - Urban and Environmental Planning"),
    ("PLAP", "PLAP - Politics-American Politics"),
    ("PLCP", "PLCP - Politics-Comparative Politics"),
    ("PLIR", "PLIR - Politics-International Relations"),
    ("PLPT", "PLPT - Politics-Political Theory"),
    ("POL", "POL - Polish"),
    ("PORT", "PORT - Portuguese"),
    ("POTR", "POTR"),
    ("PPL", "PPL - Political Philosophy, Policy, and Law"),
    ("PSHM", "PSHM - PS-Health Sciences Management"),
    ("PSLP", "PSLP - PS-Leadership Program"),
    ("PSPA", "PSPA - Professional Studies-Public Administration"),
    ("PSPM", "PSPM - Professional Studies-Project Management"),
    ("PSPS", "PSPS"),
    ("PST", "PST - Political and Social Thought"),
    ("PSYC", "PSYC - Psychology"),
    ("RELA", "RELA - Religion-African Religions"),
    ("RELB", "RELB - Religion-Buddhism"),
    ("RELC", "RELC - Religion-Christianity"),
    ("RELG", "RELG - Religion-General Religion"),
    ("RELH", "RELH - Religion-Hinduism"),
    ("RELI", "RELI - Religion-Islam"),
    ("RELJ", "RELJ - Religion-Judaism"),
    ("RELS", "RELS - Religion-Special Topic"),
    ("RUSS", "RUSS - Russian"),
    ("RUTR", "RUTR - Russian in Translation"),
    ("SANS", "SANS - Sanskrit"),
    ("SARC", "SARC - Architecture School"),
    ("SAST", "SAST - South Asian Studies"),
    ("SATR", "SATR - South Asian Literature in Translation"),
    ("SEC", "SEC - Cyber Security Analysis"),
    ("SLAV", "SLAV - Slavic"),
    ("SLTR", "SLTR"),
    ("SOC", "SOC - Sociology"),
    ("SPAN", "SPAN - Spanish"),
    ("STAT", "STAT - Statistics"),
    ("STS", "STS - Science, Technology, and Society"),
    ("SWAH", "SWAH - Swahili"),
    ("SYS", "SYS - Systems & Information Engineering"),
    ("TURK", "TURK - Turkish"),
    ("UD", "UD"),
    ("UNST", "UNST - University Studies"),
    ("URDU", "URDU - Urdu"),
    ("USEM", "USEM - University Seminar"),
    ("WGS", "WGS - Women and Gender Studies"),
]

class AdvancedSearchForm(forms.Form):
    searched_dept = forms.CharField(label='Search for a department:', widget=forms.Select(choices = dept_choices), help_text='(required)') 
    searched_catalog_num = forms.CharField(label='Search for a class by catalog number:', max_length=4, required=False, widget=forms.TextInput(attrs={'placeholder': 'ex. 1110'}))
    searched_title = forms.CharField(label='Search for a class title or keyword:', required=False, widget=forms.TextInput(attrs={'placeholder': 'ex. intro'}))

class CommentForm(forms.Form):
    comment_text = forms.CharField(label='Add a comment!', max_length=250, required=True)
    