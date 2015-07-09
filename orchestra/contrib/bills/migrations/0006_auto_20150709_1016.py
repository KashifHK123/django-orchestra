# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0005_auto_20150623_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='closed_on',
            field=models.DateField(db_index=True, blank=True, null=True, verbose_name='closed on'),
        ),
        migrations.AlterField(
            model_name='billcontact',
            name='country',
            field=models.CharField(choices=[('BS', 'Bahamas'), ('CX', 'Christmas Island'), ('DK', 'Denmark'), ('AI', 'Anguilla'), ('PF', 'French Polynesia'), ('ZA', 'South Africa'), ('NI', 'Nicaragua'), ('BB', 'Barbados'), ('TD', 'Chad'), ('PR', 'Puerto Rico'), ('AD', 'Andorra'), ('GE', 'Georgia'), ('UY', 'Uruguay'), ('AG', 'Antigua and Barbuda'), ('DM', 'Dominica'), ('RU', 'Russian Federation'), ('SE', 'Sweden'), ('UG', 'Uganda'), ('KN', 'Saint Kitts and Nevis'), ('CF', 'Central African Republic'), ('MU', 'Mauritius'), ('SR', 'Suriname'), ('KH', 'Cambodia'), ('CV', 'Cabo Verde'), ('CD', 'Congo (the Democratic Republic of the)'), ('BV', 'Bouvet Island'), ('PS', 'Palestine, State of'), ('BQ', 'Bonaire, Sint Eustatius and Saba'), ('CK', 'Cook Islands'), ('MD', 'Moldova (the Republic of)'), ('DE', 'Germany'), ('CM', 'Cameroon'), ('BF', 'Burkina Faso'), ('SM', 'San Marino'), ('NL', 'Netherlands'), ('BL', 'Saint Barthélemy'), ('SV', 'El Salvador'), ('AU', 'Australia'), ('GN', 'Guinea'), ('GM', 'Gambia'), ('MK', 'Macedonia (the former Yugoslav Republic of)'), ('MQ', 'Martinique'), ('SC', 'Seychelles'), ('GY', 'Guyana'), ('TF', 'French Southern Territories'), ('NP', 'Nepal'), ('KW', 'Kuwait'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('QA', 'Qatar'), ('JP', 'Japan'), ('HT', 'Haiti'), ('EC', 'Ecuador'), ('LR', 'Liberia'), ('RO', 'Romania'), ('LB', 'Lebanon'), ('TT', 'Trinidad and Tobago'), ('BR', 'Brazil'), ('AW', 'Aruba'), ('BM', 'Bermuda'), ('VU', 'Vanuatu'), ('MR', 'Mauritania'), ('SL', 'Sierra Leone'), ('NE', 'Niger'), ('VC', 'Saint Vincent and the Grenadines'), ('IQ', 'Iraq'), ('NC', 'New Caledonia'), ('GI', 'Gibraltar'), ('NG', 'Nigeria'), ('MX', 'Mexico'), ('NZ', 'New Zealand'), ('KP', "Korea (the Democratic People's Republic of)"), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe'), ('SX', 'Sint Maarten (Dutch part)'), ('WF', 'Wallis and Futuna'), ('CC', 'Cocos (Keeling) Islands'), ('TZ', 'Tanzania, United Republic of'), ('NU', 'Niue'), ('MP', 'Northern Mariana Islands'), ('IN', 'India'), ('LC', 'Saint Lucia'), ('TC', 'Turks and Caicos Islands'), ('PG', 'Papua New Guinea'), ('IL', 'Israel'), ('YE', 'Yemen'), ('LA', "Lao People's Democratic Republic"), ('BH', 'Bahrain'), ('NF', 'Norfolk Island'), ('DZ', 'Algeria'), ('MS', 'Montserrat'), ('JO', 'Jordan'), ('US', 'United States of America'), ('WS', 'Samoa'), ('KZ', 'Kazakhstan'), ('ME', 'Montenegro'), ('ET', 'Ethiopia'), ('UZ', 'Uzbekistan'), ('HR', 'Croatia'), ('PE', 'Peru'), ('LS', 'Lesotho'), ('UM', 'United States Minor Outlying Islands'), ('PL', 'Poland'), ('GF', 'French Guiana'), ('RW', 'Rwanda'), ('TV', 'Tuvalu'), ('FM', 'Micronesia (Federated States of)'), ('TR', 'Turkey'), ('TJ', 'Tajikistan'), ('SO', 'Somalia'), ('GP', 'Guadeloupe'), ('SG', 'Singapore'), ('JE', 'Jersey'), ('IS', 'Iceland'), ('KR', 'Korea (the Republic of)'), ('VN', 'Viet Nam'), ('SB', 'Solomon Islands'), ('CG', 'Congo'), ('NO', 'Norway'), ('VG', 'Virgin Islands (British)'), ('IT', 'Italy'), ('VE', 'Venezuela (Bolivarian Republic of)'), ('IR', 'Iran (Islamic Republic of)'), ('CO', 'Colombia'), ('IM', 'Isle of Man'), ('GQ', 'Equatorial Guinea'), ('UA', 'Ukraine'), ('MN', 'Mongolia'), ('GH', 'Ghana'), ('BO', 'Bolivia (Plurinational State of)'), ('AR', 'Argentina'), ('GB', 'United Kingdom of Great Britain and Northern Ireland'), ('TK', 'Tokelau'), ('PT', 'Portugal'), ('CW', 'Curaçao'), ('BN', 'Brunei Darussalam'), ('AM', 'Armenia'), ('TL', 'Timor-Leste'), ('TO', 'Tonga'), ('MY', 'Malaysia'), ('AX', 'Åland Islands'), ('CY', 'Cyprus'), ('GL', 'Greenland'), ('RS', 'Serbia'), ('AF', 'Afghanistan'), ('LT', 'Lithuania'), ('KY', 'Cayman Islands'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('CN', 'China'), ('CL', 'Chile'), ('BA', 'Bosnia and Herzegovina'), ('DO', 'Dominican Republic'), ('CH', 'Switzerland'), ('LV', 'Latvia'), ('HN', 'Honduras'), ('TH', 'Thailand'), ('GT', 'Guatemala'), ('SY', 'Syrian Arab Republic'), ('BT', 'Bhutan'), ('GS', 'South Georgia and the South Sandwich Islands'), ('YT', 'Mayotte'), ('MV', 'Maldives'), ('LY', 'Libya'), ('MG', 'Madagascar'), ('FI', 'Finland'), ('AE', 'United Arab Emirates'), ('ID', 'Indonesia'), ('AS', 'American Samoa'), ('IO', 'British Indian Ocean Territory'), ('RE', 'Réunion'), ('SH', 'Saint Helena, Ascension and Tristan da Cunha'), ('ES', 'Spain'), ('MZ', 'Mozambique'), ('PN', 'Pitcairn'), ('DJ', 'Djibouti'), ('LI', 'Liechtenstein'), ('BZ', 'Belize'), ('EE', 'Estonia'), ('MF', 'Saint Martin (French part)'), ('PW', 'Palau'), ('TM', 'Turkmenistan'), ('AL', 'Albania'), ('MO', 'Macao'), ('AO', 'Angola'), ('VA', 'Holy See'), ('SN', 'Senegal'), ('GG', 'Guernsey'), ('MH', 'Marshall Islands'), ('NR', 'Nauru'), ('KE', 'Kenya'), ('BJ', 'Benin'), ('MA', 'Morocco'), ('EG', 'Egypt'), ('KG', 'Kyrgyzstan'), ('GD', 'Grenada'), ('IE', 'Ireland'), ('BG', 'Bulgaria'), ('HU', 'Hungary'), ('SD', 'Sudan'), ('NA', 'Namibia'), ('CU', 'Cuba'), ('BY', 'Belarus'), ('GR', 'Greece'), ('TW', 'Taiwan (Province of China)'), ('MT', 'Malta'), ('ST', 'Sao Tome and Principe'), ('JM', 'Jamaica'), ('BW', 'Botswana'), ('MM', 'Myanmar'), ('KI', 'Kiribati'), ('SA', 'Saudi Arabia'), ('FK', 'Falkland Islands  [Malvinas]'), ('FR', 'France'), ('VI', 'Virgin Islands (U.S.)'), ('GA', 'Gabon'), ('ML', 'Mali'), ('LK', 'Sri Lanka'), ('FO', 'Faroe Islands'), ('CI', "Côte d'Ivoire"), ('LU', 'Luxembourg'), ('TN', 'Tunisia'), ('PA', 'Panama'), ('HK', 'Hong Kong'), ('TG', 'Togo'), ('KM', 'Comoros'), ('PH', 'Philippines'), ('PM', 'Saint Pierre and Miquelon'), ('AQ', 'Antarctica'), ('MW', 'Malawi'), ('MC', 'Monaco'), ('FJ', 'Fiji'), ('BI', 'Burundi'), ('PY', 'Paraguay'), ('SJ', 'Svalbard and Jan Mayen'), ('HM', 'Heard Island and McDonald Islands'), ('SS', 'South Sudan'), ('CZ', 'Czech Republic'), ('GU', 'Guam'), ('SZ', 'Swaziland'), ('GW', 'Guinea-Bissau'), ('CA', 'Canada'), ('EH', 'Western Sahara'), ('OM', 'Oman'), ('ER', 'Eritrea'), ('BE', 'Belgium'), ('CR', 'Costa Rica'), ('PK', 'Pakistan'), ('BD', 'Bangladesh')], default='ES', verbose_name='country', max_length=20),
        ),
        migrations.AlterField(
            model_name='billline',
            name='end_on',
            field=models.DateField(blank=True, null=True, verbose_name='end'),
        ),
    ]
