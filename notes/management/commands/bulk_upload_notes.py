from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from notes.models import Subject, Chapter, Topic, Note


class Command(BaseCommand):
    help = 'Bulk upload notes from a local folder'

    def add_arguments(self, parser):
        parser.add_argument('folder', type=str, help='Path to folder containing note images')
        parser.add_argument('--subject', type=str, required=True, help='Subject name')
        parser.add_argument('--chapter', type=int, required=True, help='Chapter number')
        parser.add_argument('--topic', type=int, required=True, help='Topic number')

    def handle(self, *args, **options):
        folder = Path(options['folder'])
        subject_name = options['subject']
        chapter_num = options['chapter']
        topic_num = options['topic']

        if not folder.exists():
            raise CommandError(f'Folder does not exist: {folder}')

        # Get or create subject
        subject, _ = Subject.objects.get_or_create(
            name=subject_name,
            defaults={'description': f'Notes for {subject_name}', 'order': 1}
        )
        self.stdout.write(f'Subject: {subject.name}')

        # Get or create chapter
        chapter, _ = Chapter.objects.get_or_create(
            subject=subject,
            chapter_number=chapter_num,
            defaults={'title': f'Chapter {chapter_num}', 'description': ''}
        )
        self.stdout.write(f'Chapter: {chapter.title}')

        # Get or create topic
        topic, _ = Topic.objects.get_or_create(
            chapter=chapter,
            topic_number=topic_num,
            defaults={'title': f'Topic {topic_num}', 'description': ''}
        )
        self.stdout.write(f'Topic: {topic.title}')

        # Upload all images in folder
        image_extensions = ('.jpg', '.jpeg', '.png', '.webp')
        images = [f for f in folder.iterdir() if f.suffix.lower() in image_extensions]

        if not images:
            raise CommandError(f'No images found in {folder}')

        self.stdout.write(f'Found {len(images)} images to upload')

        for i, img_path in enumerate(sorted(images), start=1):
            self.stdout.write(f'Uploading {img_path.name}...')

            with open(img_path, 'rb') as f:
                note = Note.objects.create(
                    topic=topic,
                    title=img_path.stem,
                    page_number=i,
                    description=''
                )
                note.image.save(
                    img_path.name,
                    ContentFile(f.read()),
                    save=True
                )

            self.stdout.write(self.style.SUCCESS(f'  ✓ Uploaded: {img_path.name}'))

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully uploaded {len(images)} notes!'))
