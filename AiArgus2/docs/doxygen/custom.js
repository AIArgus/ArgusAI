// Language Switcher Implementation
document.addEventListener('DOMContentLoaded', function() {
    // Create language switcher element
    const switcher = document.createElement('div');
    switcher.className = 'language-switcher';
    switcher.innerHTML = `
        <select id="language-select">
            <option value="en">English</option>
            <option value="pl">Polski</option>
        </select>
    `;
    document.body.appendChild(switcher);

    // Get language from localStorage or default to English
    const currentLang = localStorage.getItem('preferred-language') || 'en';
    document.documentElement.lang = currentLang;
    document.getElementById('language-select').value = currentLang;

    // Language switch handler
    document.getElementById('language-select').addEventListener('change', function(e) {
        const newLang = e.target.value;
        document.documentElement.lang = newLang;
        localStorage.setItem('preferred-language', newLang);
    });

    // Add language attributes to all content
    function addLanguageAttributes() {
        // Process all text nodes
        const walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );

        let node;
        while (node = walker.nextNode()) {
            if (node.nodeValue.trim()) {
                const span = document.createElement('span');
                span.lang = 'en';
                span.className = 'block';
                node.parentNode.insertBefore(span, node);
                span.appendChild(node);
            }
        }

        // Process all elements
        const elements = document.getElementsByTagName('*');
        for (let element of elements) {
            if (!element.hasAttribute('lang') && element.textContent.trim()) {
                element.lang = 'en';
            }
        }
    }

    // Initialize language attributes
    addLanguageAttributes();
}); 