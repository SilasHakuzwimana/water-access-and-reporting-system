// Add interactivity for highlighting active sidebar item
const sidebarItems = document.querySelectorAll('.sidebar nav ul li');
const actionDescriptions = document.querySelectorAll('.action-description');

sidebarItems.forEach((item, index) => {
    item.addEventListener('click', () => {
        // Highlight the active item
        sidebarItems.forEach(i => i.style.backgroundColor = '#fff');
        item.style.backgroundColor = '#fff';

        // Show corresponding action description
        actionDescriptions.forEach(desc => desc.style.display = 'none');
        actionDescriptions[index].style.display = 'block';
    });
});

// Initially show the first action description
actionDescriptions.forEach((desc, index) => {
    desc.style.display = index === 0 ? 'block' : 'none';
});
