document.addEventListener('DOMContentLoaded', async () => {
    const addFolderButton = document.getElementById('add-folder');
    const burgerMenu = document.querySelector('.burger-container');
    const confirmButton = document.querySelector('.confirm')
    const addFolderMenu = document.querySelector('.add-folder-menu')
    let menuStatus = false;
    var colorWheel = new ReinventedColorWheel({
        appendTo: document.querySelector('.color-container'),
        wheelDiameter: 450,
        wheelThickness: 40,
        handleDiameter: 16,
        wheelReflectsSaturation: false,
    })

    async function main() {
        const images = await getImages();
        if (images) {
            hideAddFolderButton();
            const folders = await getFolders();
            renderImages(images, folders);
        }
    }

    addFolderMenu.addEventListener('click', async () => {
        try {
            const path = await window.dialog.openFolder();
            if (path[0]) {
                const folderId = await addFolder(path[0]);
                await scan(folderId);
                const images = await getImages();
                const folders = await getFolders();
                renderImages(images, folders);
                initializeViews();
            }
        } catch (error) {
            alert("Error adding folder:", error);
        }
    });

    addFolderButton.addEventListener('click', async () => {
        try {
            const path = await window.dialog.openFolder();
            if (path[0]) {
                const folderId = await addFolder(path[0]);
                await scan(folderId);
                const images = await getImages();
                const folders = await getFolders();
                renderImages(images, folders);
                initializeViews();
            }
        } catch (error) {
            alert("Error adding folder:", error);
        }
    });

    burgerMenu.addEventListener('click', async () => {
        const filterMenu = document.querySelector('.menu')
        if (menuStatus) {
            filterMenu.style.visibility = "hidden";
            menuStatus = false;
        } else {
            filterMenu.style.visibility = "visible";
            menuStatus = true;
        }
    });

    confirmButton.addEventListener('click', async () => {
        const sortedImages = await getSortedimages(colorWheel.rgb);
        const folders = await getFolders();
        renderImages(sortedImages, folders)
    });

    await main();
});

async function getSortedimages(color) {
    try {
        const response = await axios.post("http://127.0.0.1:8080/api/sort/", {color: color});
        return response.data;
    } catch (error) {
        alert("Error sorting images:", error);
    }
}

async function addFolder(path) {
    try {
        const response = await axios.post("http://127.0.0.1:8080/api/folder/", { path: path });
        return response.data.id;
    } catch (error) {
        alert("Error posting folder:", error);
    }
}

async function getFolders() {
    try {
        const response = await axios.get("http://127.0.0.1:8080/api/folder/");
        return response.data;
    } catch (error) {
        alert("Error getting folders:", error);
    }
}

async function scan(folderId) {
    try {
        await axios.get(`http://127.0.0.1:8080/api/scan/?folder=${folderId}`);
    } catch (error) {
        alert("Error scanning folder:", error);
    }
}

async function getImages() {
    try {
        const response = await axios.get("http://127.0.0.1:8080/api/image/");
        return response.data;
    } catch (error) {
        alert("Error getting images:", error);
    }
}

function hideAddFolderButton() {
    const addFolderButtonContainer = document.querySelector(".add-folder-button");
    if (addFolderButtonContainer) {
        addFolderButtonContainer.remove();
    }
}

function getFolderPath(folders, folderId) {
    const folder = folders.find(folder => folder.id === folderId);
    return folder ? folder.path : '';
}

let viewer;

function renderImages(images, folders) {
    const imagesContainer = document.querySelector(".images");
    imagesContainer.innerHTML = '';
    images.forEach(image => {
        const filePath = getFolderPath(folders, image.folder_id) + "\\" + image.filename;
        const imageElement = `
            <li class="image-container">
                <img src="${filePath}" alt="${image.filename}" id="${image.id}" class="image" height="200" decoding="async">
            </li>
        `;
        imagesContainer.innerHTML += imageElement;
    });
    const gallery = document.querySelector('.images-container');

    if (viewer) {
        viewer.destroy();
    }
    viewer = new Viewer(gallery);
}
