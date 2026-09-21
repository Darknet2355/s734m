"""
Seeds the database with realistic demo/sample data for FutureForge Labs.

Usage:
    python manage.py seed_demo_data
    python manage.py seed_demo_data --flush   (wipes existing demo content first)

All records are clearly placeholder/demo data — replace or delete them from
the admin dashboard once real content is ready.
"""
import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from blog.models import BlogCategory, BlogPost, Tag
from core.placeholder_images import make_placeholder_image
from institutions.models import Institution
from inquiries.models import ContactMessage, TrainingRequest
from media_gallery.models import MediaItem
from programs.models import Program, ProgramCategory
from projects.models import Project, ProjectImage
from services.models import Service
from team.models import SocialLink, TeamMember
from technologies.models import TechCategory, Technology

User = get_user_model()


class Command(BaseCommand):
    help = "Seed the database with realistic FutureForge Labs demo/sample data."

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush', action='store_true',
            help='Delete existing demo content before reseeding.'
        )

    def handle(self, *args, **options):
        if options['flush']:
            self.stdout.write('Flushing existing demo content...')
            for model in [MediaItem, BlogPost, Tag, BlogCategory, Project, Institution,
                          Service, TeamMember, Technology, TechCategory, Program, ProgramCategory]:
                model.objects.all().delete()

        self.create_superuser()
        program_categories = self.create_program_categories()
        self.create_programs(program_categories)
        tech_categories = self.create_tech_categories()
        technologies = self.create_technologies(tech_categories)
        programs = list(Program.objects.all())
        self.create_institutions(programs)
        self.create_projects(technologies)
        self.create_services()
        self.create_team()
        self.create_blog()
        self.create_media()

        self.stdout.write(self.style.SUCCESS(
            '\nDemo data seeded successfully! All records are sample/demo content — '
            'edit or delete them from /django-admin/ or the dashboard.'
        ))

    # ------------------------------------------------------------------
    def create_superuser(self):
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin', email='admin@futureforgelabs.org', password='FutureForge2026!'
            )
            self.stdout.write(self.style.SUCCESS(
                "Created superuser -> username: admin / password: FutureForge2026!"
            ))
        else:
            self.stdout.write('Superuser already exists, skipping.')

    # ------------------------------------------------------------------
    def create_program_categories(self):
        names = ['Primary School', 'Secondary School', 'University / College', 'Professional / Organizations']
        cats = {}
        for i, name in enumerate(names):
            cat, _ = ProgramCategory.objects.get_or_create(
                name=name, defaults={'slug': slugify(name), 'order': i, 'description': f'Programs designed for {name.lower()}.'}
            )
            cats[name] = cat
        return cats

    def create_programs(self, cats):
        if Program.objects.exists():
            self.stdout.write('Programs already exist, skipping.')
            return
        data = [
            ('Introduction to Coding', cats['Primary School'], 'beginner', 'Ages 8-12',
             '4 weeks', 'Block-based coding\nLogical thinking\nProblem solving',
             'A playful first step into programming using block-based tools, building simple animations and games.'),
            ('Robotics for Beginners', cats['Primary School'], 'beginner', 'Ages 9-13',
             '6 weeks', 'Basic robot assembly\nSimple sensors\nTeamwork',
             'Learners assemble and program simple robots, discovering how motors and sensors work together.'),
            ('Arduino Programming', cats['Secondary School'], 'beginner', 'Grade 8-10',
             '5 weeks', 'C++ basics\nCircuits\nDigital & analog I/O',
             'A hands-on introduction to the Arduino platform — wiring circuits and writing real embedded code.'),
            ('Python Programming', cats['Secondary School'], 'intermediate', 'Grade 9-12',
             '8 weeks', 'Python syntax\nData structures\nMini projects',
             'Learners build a solid Python foundation through practical mini-projects and challenges.'),
            ('Internet of Things (IoT)', cats['Secondary School'], 'intermediate', 'Grade 10-12',
             '6 weeks', 'IoT protocols\nCloud dashboards\nSensor networks',
             'Students connect sensors to the cloud and build simple IoT dashboards to visualize live data.'),
            ('Embedded Systems & ESP32', cats['University / College'], 'intermediate', 'University students',
             '10 weeks', 'Embedded C\nRTOS basics\nESP32 development',
             'A deep dive into embedded systems design using the ESP32, covering firmware and low-level I/O.'),
            ('Artificial Intelligence & Machine Learning', cats['University / College'], 'advanced', 'University students',
             '12 weeks', 'Python for AI\nModel training\nDeployment basics',
             'From foundational ML concepts to training and deploying simple models on real datasets.'),
            ('Corporate Technology Training', cats['Professional / Organizations'], 'intermediate', 'Working professionals',
             '3 days intensive', 'Digital literacy\nAutomation tools\nInnovation mindset',
             'A fast-paced program helping teams adopt practical automation and emerging technology skills.'),
        ]
        for i, (title, cat, level, audience, duration, skills, desc) in enumerate(data):
            program = Program.objects.create(
                title=title, category=cat, description=desc, target_audience=audience,
                duration=duration, skills_acquired=skills, difficulty_level=level,
                status='active', is_featured=(i < 3),
            )
            program.image.save(f'{program.slug}.png', make_placeholder_image(title), save=True)
        self.stdout.write(self.style.SUCCESS(f'Created {len(data)} programs.'))

    # ------------------------------------------------------------------
    def create_tech_categories(self):
        names = ['Microcontrollers', 'Single-Board Computers', 'Components & Sensors', 'Robotics Kits']
        cats = {}
        for i, name in enumerate(names):
            cat, _ = TechCategory.objects.get_or_create(name=name, defaults={'slug': slugify(name), 'order': i})
            cats[name] = cat
        return cats

    def create_technologies(self, cats):
        if Technology.objects.exists():
            self.stdout.write('Technologies already exist, skipping.')
            return list(Technology.objects.all())
        data = [
            ('Arduino Uno', cats['Microcontrollers'], 'beginner', 'Robotics\nAutomation\nSensors\nEmbedded systems\nEducation',
             'The classic beginner-friendly microcontroller board, ideal for learning circuits and embedded programming.'),
            ('Arduino Nano', cats['Microcontrollers'], 'beginner', 'Compact robotics\nWearables\nSensor projects',
             'A compact Arduino variant perfect for space-constrained projects and portable builds.'),
            ('Arduino Mega', cats['Microcontrollers'], 'intermediate', 'Complex robotics\nMulti-sensor systems\n3D printers',
             'An Arduino board with more I/O pins for larger, multi-sensor and multi-actuator projects.'),
            ('ESP32', cats['Microcontrollers'], 'intermediate', 'IoT\nRobotics\nWi-Fi/Bluetooth projects\nHome automation',
             'A powerful Wi-Fi and Bluetooth-enabled microcontroller central to most of our IoT training.'),
            ('ESP8266', cats['Microcontrollers'], 'beginner', 'IoT\nSmart devices\nSensor dashboards',
             'A low-cost Wi-Fi microcontroller widely used for simple connected-device projects.'),
            ('Raspberry Pi', cats['Single-Board Computers'], 'intermediate', 'AI\nRobotics\nAutomation\nMedia servers',
             'A full single-board computer used for AI, robotics control and advanced automation projects.'),
            ('Raspberry Pi Pico', cats['Single-Board Computers'], 'beginner', 'Embedded projects\nRobotics\nSensor logging',
             'A low-cost microcontroller board from the Raspberry Pi family, great for embedded learning.'),
            ('Micro:bit', cats['Single-Board Computers'], 'beginner', 'Primary/secondary education\nWearables\nSimple robotics',
             'A pocket-sized computer designed for beginners, popular in primary and secondary classrooms.'),
            ('Sensors & Motor Drivers', cats['Components & Sensors'], 'beginner', 'Robotics\nAutomation\nSmart systems',
             'A range of ultrasonic, temperature, motion and light sensors plus motor driver modules used across our projects.'),
            ('Robotics Kits', cats['Robotics Kits'], 'beginner', 'Robotics competitions\nSTEAM clubs\nSchool programs',
             'Complete chassis, wheel and sensor kits used to build line-following and obstacle-avoidance robots.'),
        ]
        created = []
        for name, cat, level, apps, desc in data:
            tech = Technology.objects.create(
                name=name, category=cat, description=desc, applications=apps,
                difficulty=level, training_level='Secondary School to University', is_featured=True,
            )
            tech.image.save(f'{tech.slug}.png', make_placeholder_image(name), save=True)
            created.append(tech)
        self.stdout.write(self.style.SUCCESS(f'Created {len(created)} technologies.'))
        return created

    # ------------------------------------------------------------------
    def create_institutions(self, programs):
        if Institution.objects.exists():
            self.stdout.write('Institutions already exist, skipping.')
            return
        data = [
            ('Kampala Innovation High School', 'school', 'Kampala, Uganda',
             'A secondary school partnering with FutureForge Labs to run weekly robotics and coding clubs.'),
            ('Makerere Technology Institute', 'university', 'Kampala, Uganda',
             'A university partner hosting our embedded systems and AI training tracks for engineering students.'),
            ('BrightPath Community Center', 'community', 'Jinja, Uganda',
             'A community organization running holiday STEAM camps for out-of-school youth.'),
            ('NovaTech Solutions Ltd', 'company', 'Kampala, Uganda',
             'A technology company that sponsors staff upskilling workshops in IoT and automation.'),
            ('Youth Innovation Hub', 'innovation_hub', 'Mbarara, Uganda',
             'An innovation hub providing space and mentorship for youth-led hardware prototypes.'),
        ]
        for name, itype, location, desc in data:
            inst = Institution.objects.create(
                name=name, type=itype, location=location, description=desc,
                partnership_info='Ongoing training partnership since 2024, including on-site workshops and equipment loans.',
            )
            inst.logo.save(f'{inst.slug}-logo.png', make_placeholder_image(name, size=(400, 400)), save=True)
            if programs:
                inst.programs_conducted.set(programs[:2])
        self.stdout.write(self.style.SUCCESS('Created 5 institutions.'))

    # ------------------------------------------------------------------
    def create_projects(self, technologies):
        if Project.objects.exists():
            self.stdout.write('Projects already exist, skipping.')
            return
        tech_by_name = {t.name: t for t in technologies} if technologies else {}
        data = [
            ('Autonomous Navigation Robot', 'robotics', 'university',
             'A robot that maps and navigates a room autonomously using ultrasonic sensors and a Raspberry Pi.',
             ['Raspberry Pi', 'Sensors & Motor Drivers']),
            ('Smart Waste Sorting System', 'automation', 'secondary',
             'An ESP32-powered system that sorts recyclable waste using sensors and a simple sorting arm.',
             ['ESP32', 'Sensors & Motor Drivers']),
            ('AI Homework Assistant', 'ai', 'secondary',
             'A simple AI-powered chatbot prototype that helps students with revision questions.',
             ['Raspberry Pi']),
            ('Line Following Robot', 'robotics', 'primary',
             'A classic beginner robotics build that follows a black line using IR sensors.',
             ['Arduino Uno', 'Robotics Kits']),
            ('Smart Agriculture System', 'iot', 'university',
             'A soil-moisture and weather-aware irrigation system built with ESP32 and cloud dashboards.',
             ['ESP32', 'Sensors & Motor Drivers']),
            ('IoT Weather Station', 'iot', 'secondary',
             'A connected weather station reporting temperature, humidity and pressure to a live dashboard.',
             ['ESP8266', 'Sensors & Motor Drivers']),
            ('Obstacle Avoidance Robot', 'robotics', 'primary',
             'An ultrasonic-sensor robot that detects and avoids obstacles in real time.',
             ['Arduino Uno', 'Sensors & Motor Drivers']),
            ('Smart Home System', 'iot', 'professional',
             'A prototype home-automation system controlling lights and appliances from a mobile dashboard.',
             ['ESP32', 'Raspberry Pi']),
        ]
        for i, (title, category, audience, desc, tech_names) in enumerate(data):
            project = Project(
                title=title, description=desc, category=category, target_audience=audience,
                project_date=datetime.date.today() - datetime.timedelta(days=i * 20),
                status='published', is_featured=(i < 3),
            )
            project.featured_image.save(f'{slugify(title)}.png', make_placeholder_image(title), save=False)
            project.save()
            for name in tech_names:
                if name in tech_by_name:
                    project.technologies.add(tech_by_name[name])
            gallery_img = ProjectImage(project=project, caption=f'{title} — build process')
            gallery_img.image.save(f'{slugify(title)}-gallery-1.png', make_placeholder_image(f'{title} Gallery'), save=False)
            gallery_img.save()
        self.stdout.write(self.style.SUCCESS(f'Created {len(data)} projects.'))

    # ------------------------------------------------------------------
    def create_services(self):
        if Service.objects.exists():
            self.stdout.write('Services already exist, skipping.')
            return
        data = [
            ('STEAM Training', 'fa-solid fa-atom', 'Schools\nCommunity organizations',
             'Practical Science, Technology, Engineering, Arts and Mathematics training for young learners.',
             'Hands-on learning\nCross-disciplinary skills\nEngaged, confident learners'),
            ('School Robotics Programs', 'fa-solid fa-robot', 'Primary schools\nSecondary schools',
             'Ongoing robotics clubs and curricula integrated into the school calendar.',
             'Regular practical sessions\nCompetition readiness\nTeam-building'),
            ('Teacher Training', 'fa-solid fa-chalkboard-user', 'Teachers\nSchool administrators',
             'Equipping educators to confidently teach robotics, coding and electronics themselves.',
             'Sustainable in-house capacity\nUpdated teaching methods\nHands-on trainer certification'),
            ('Corporate Technology Training', 'fa-solid fa-building', 'Companies\nGovernment organizations',
             'Upskilling teams in automation, IoT and digital tools relevant to their industry.',
             'Practical, job-relevant skills\nImproved digital capacity\nCustom curricula'),
            ('Arduino & ESP32 Training', 'fa-solid fa-microchip', 'Students\nHobbyists\nEngineers',
             'Focused, hands-on training on Arduino and ESP32 development for embedded projects.',
             'Real hardware experience\nProject-based learning\nCertificate of completion'),
            ('AI & Machine Learning Training', 'fa-solid fa-brain', 'University students\nProfessionals',
             'Practical AI/ML training from foundational concepts to simple deployed models.',
             'Real datasets\nModel deployment basics\nIndustry-relevant skills'),
            ('IoT Development Services', 'fa-solid fa-wifi', 'Companies\nInnovation hubs',
             'Design and prototyping of connected IoT solutions for real business or research problems.',
             'End-to-end prototyping\nCloud dashboard integration\nScalable design'),
            ('Technology Consultancy', 'fa-solid fa-comments', 'NGOs\nGovernment organizations\nCompanies',
             'Strategic guidance on adopting practical technology and STEAM programs within your organization.',
             'Tailored recommendations\nBudget-conscious planning\nImplementation support'),
        ]
        for title, icon, clients, desc, benefits in data:
            service = Service.objects.create(
                title=title, icon_class=icon, description=desc,
                target_clients=clients, benefits=benefits, is_active=True,
            )
            service.image.save(f'{service.slug}.png', make_placeholder_image(title), save=True)
        self.stdout.write(self.style.SUCCESS(f'Created {len(data)} services.'))

    # ------------------------------------------------------------------
    def create_team(self):
        if TeamMember.objects.exists():
            self.stdout.write('Team members already exist, skipping.')
            return
        data = [
            ('Amara Nakato', 'Founder / Director', 'Leads FutureForge Labs\u2019 strategy and institutional partnerships.',
             'Amara founded FutureForge Labs to bring practical technology education to underserved schools. '
             'With a background in electrical engineering and over a decade in EdTech, she leads partnerships '
             'with schools, universities and organizations across the region.',
             'Strategic Leadership\nSTEAM Curriculum Design\nPartnerships'),
            ('Daniel Okello', 'Robotics Engineer', 'Designs and builds the robotics kits used in our training programs.',
             'Daniel is a robotics engineer with hands-on experience building competition robots and training kits. '
             'He leads the design of every robotics program at FutureForge Labs, from beginner kits to advanced builds.',
             'Robotics Design\nMechatronics\nArduino & ESP32'),
            ('Grace Atim', 'AI & Machine Learning Trainer', 'Trains university learners in practical AI and ML skills.',
             'Grace holds a background in computer science and specializes in making machine learning approachable '
             'for beginners, guiding learners from Python basics to their first trained models.',
             'Machine Learning\nPython\nData Science'),
            ('Brian Musoke', 'Software Developer', 'Builds the software tools and dashboards used across our IoT programs.',
             'Brian is a full-stack developer who builds the internal tools, dashboards and IoT integrations that '
             'power FutureForge Labs\u2019 training programs and demos.',
             'Web Development\nIoT Dashboards\nDjango & Python'),
            ('Patricia Nabirye', 'STEAM Trainer', 'Delivers hands-on STEAM sessions for primary and secondary learners.',
             'Patricia is a passionate educator who has trained hundreds of primary and secondary students in coding, '
             'electronics and robotics fundamentals through fun, hands-on sessions.',
             'STEAM Education\nClassroom Facilitation\nCurriculum Delivery'),
        ]
        for i, (name, position, short_bio, full_bio, expertise) in enumerate(data):
            member = TeamMember.objects.create(
                full_name=name, position=position, short_bio=short_bio, full_bio=full_bio,
                areas_of_expertise=expertise, order=i, is_active=True,
            )
            member.photo.save(f'{member.slug}.png', make_placeholder_image(name, size=(500, 500)), save=True)
            SocialLink.objects.create(team_member=member, platform='linkedin', url='https://linkedin.com/company/futureforgelabs')
        self.stdout.write(self.style.SUCCESS(f'Created {len(data)} team members.'))

    # ------------------------------------------------------------------
    def create_blog(self):
        if BlogPost.objects.exists():
            self.stdout.write('Blog posts already exist, skipping.')
            return
        cat_names = ['STEAM Education', 'Robotics', 'Artificial Intelligence', 'Arduino', 'Programming', 'Student Achievements']
        cats = {}
        for name in cat_names:
            cat, _ = BlogCategory.objects.get_or_create(name=name, defaults={'slug': slugify(name)})
            cats[name] = cat

        author = User.objects.filter(is_superuser=True).first()

        data = [
            ('Why Hands-On STEAM Education Matters More Than Ever', cats['STEAM Education'],
             'Practical, project-based learning builds skills that lecture-only classrooms simply cannot.',
             'In classrooms across the region, we are seeing a shift from theory-only STEAM lessons toward '
             'hands-on, project-based learning. At FutureForge Labs, every session ends with learners building '
             'something real — and that changes how they engage with the material entirely.\n\n'
             'This post explores why practical learning sticks, how it builds problem-solving confidence, and '
             'what schools can do to bring more hands-on STEAM into their existing curriculum.'),
            ('5 Beginner Robotics Projects Every Student Should Try', cats['Robotics'],
             'From line followers to obstacle avoiders — these builds are the perfect entry point into robotics.',
             'Getting started in robotics can feel overwhelming, but a handful of classic beginner projects can '
             'take any student from zero to confident builder. In this post, we walk through five projects we use '
             'in our own beginner robotics program, including the line-following robot and the obstacle-avoidance robot.'),
            ('Demystifying Artificial Intelligence for Young Learners', cats['Artificial Intelligence'],
             'AI does not need to be intimidating — here is how we introduce it to secondary school students.',
             'Artificial intelligence can sound intimidating, especially to younger learners. In our AI Basics '
             'sessions, we break the topic down into approachable, hands-on activities that show students exactly '
             'how a simple model "learns" from data — no advanced math required.'),
            ('Getting Started with Arduino: A Beginner\u2019s Guide', cats['Arduino'],
             'Everything a first-time learner needs to know before their first Arduino project.',
             'Arduino remains one of the best ways to introduce learners to embedded electronics. This guide '
             'covers what you need, from your first LED blink sketch to reading a basic sensor, based on how we '
             'structure our own beginner Arduino training.'),
            ('Python vs Block-Based Coding: When to Make the Switch', cats['Programming'],
             'A practical guide for educators deciding when learners are ready to move beyond block-based tools.',
             'Block-based coding tools are a fantastic starting point, but at some stage learners are ready for '
             'text-based programming. We share the signs we look for in our own secondary school Python program, '
             'and how we structure the transition to keep learners confident.'),
            ('Celebrating Our Learners: Regional Robotics Competition Highlights', cats['Student Achievements'],
             'FutureForge Labs students showcased their robotics builds at this year\u2019s regional competition.',
             'We are incredibly proud of the students from our partner schools who competed in this year\u2019s '
             'regional robotics competition. Their line-following and obstacle-avoidance robots — built entirely '
             'during our after-school program — performed brilliantly, and several teams placed in the top ranks.'),
        ]
        for title, cat, excerpt, content in data:
            post = BlogPost.objects.create(
                title=title, author=author, category=cat, excerpt=excerpt, content=content, status='published',
            )
            post.featured_image.save(f'{post.slug}.png', make_placeholder_image(title), save=True)
        self.stdout.write(self.style.SUCCESS(f'Created {len(data)} blog posts.'))

    # ------------------------------------------------------------------
    def create_media(self):
        if MediaItem.objects.exists():
            self.stdout.write('Media items already exist, skipping.')
            return
        data = [
            ('Robotics Workshop — Line Followers in Action', 'image', 'robotics', 'Students testing their line-following robots.'),
            ('Arduino Basics Training Session', 'image', 'arduino', 'A beginner Arduino session with secondary school students.'),
            ('AI Basics Demo Day', 'image', 'ai', 'Students presenting their simple AI demo projects.'),
            ('FutureForge Labs Training Highlights', 'video', 'training', 'A short highlight reel from our recent training sessions.'),
            ('Regional Robotics Competition 2026', 'video', 'events', 'Highlights from the regional robotics competition.'),
            ('Electronics Workshop — Circuit Building', 'image', 'electronics', 'Hands-on circuit-building session for beginners.'),
        ]
        for title, mtype, category, desc in data:
            item = MediaItem(title=title, media_type=mtype, category=category, description=desc, is_published=True)
            if mtype == 'video':
                item.video_url = 'https://www.youtube.com/embed/dQw4w9WgXcQ'
                item.save()
            else:
                item.image.save(f'{slugify(title)}.png', make_placeholder_image(title), save=False)
                item.save()
        self.stdout.write(self.style.SUCCESS(f'Created {len(data)} media items.'))
