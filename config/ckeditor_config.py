# ckeditor_config.py

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading', '|',
            'bold', 'italic', 'underline', '|',
            'fontSize', 'fontFamily','|',
            'bulletedList', 'numberedList', '|',
        ],
        'fontSize': {
            'options': [10, 12, 14, 'default', 18, 20, 24]
        },
        'fontFamily': {
            'options': [
                'default',
                'Arial, Helvetica, sans-serif',
                'Times New Roman, Times, serif',
                'Courier New, Courier, monospace'
            ]
        }
    }
}
