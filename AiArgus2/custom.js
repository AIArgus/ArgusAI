// Language Switcher Implementation
document.addEventListener('DOMContentLoaded', function() {
    // Create language switcher element
    const switcher = document.createElement('div');
    switcher.className = 'language-switcher';
    
    const select = document.createElement('select');
    select.innerHTML = `
        <option value="en">English</option>
        <option value="pl">Polski</option>
    `;
    
    // Set initial language based on browser settings or default to English
    const savedLang = localStorage.getItem('preferredLanguage') || navigator.language.split('-')[0];
    select.value = savedLang;
    document.documentElement.lang = savedLang;
    
    // Add event listener for language change
    select.addEventListener('change', function(e) {
        const newLang = e.target.value;
        document.documentElement.lang = newLang;
        localStorage.setItem('preferredLanguage', newLang);
    });
    
    switcher.appendChild(select);
    document.body.appendChild(switcher);
    
    // Add language attributes to all content elements
    const contentElements = document.querySelectorAll('h1, h2, h3, h4, h5, h6, p, li, td, th, div.title, div.contents');
    contentElements.forEach(element => {
        if (!element.hasAttribute('lang')) {
            element.setAttribute('lang', 'en');
        }
    });
}); 