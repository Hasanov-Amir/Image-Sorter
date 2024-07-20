document.addEventListener('DOMContentLoaded', async () => {
    let page = 1;
    let sorted = false;
    const addFolderButton = document.getElementById('add-folder');
    const burgerMenu = document.querySelector('.burger-container');
    const confirmButton = document.querySelector('.confirm');
    const addFolderMenu = document.querySelector('.add-folder-menu');
    let menuStatus = false;
    var colorWheel = new ReinventedColorWheel({
        appendTo: document.querySelector('.color-container'),
        wheelDiameter: 450,
        wheelThickness: 40,
        handleDiameter: 16,
        wheelReflectsSaturation: false,
    });

    async function main() {
        page = 1
        const images = await getImages(page);
        if (images.images) {
            hideAddFolderButton();
            const folders = await getFolders();
            renderImages(images.images, folders);
        }
    }

    window.addEventListener("scroll", async () => {
        const endOfPage = window.innerHeight + window.scrollY >= document.querySelector('body').scrollHeight;
        if (endOfPage) {
            if (sorted) {
                page++
                const images = await getSortedimages(colorWheel.rgb, page)
                const folders = await getFolders();
                renderImages(images.images, folders, false)
            } else {
                page++
                const images = await getImages(page)
                const folders = await getFolders();
                renderImages(images.images, folders, false)
            }
        }
    });

    addFolderMenu.addEventListener('click', async () => {
        page = 1
        try {
            const path = await window.dialog.openFolder();
            if (path[0]) {
                const folderId = await addFolder(path[0]);
                await scan(folderId);
                const images = await getImages(page);
                const folders = await getFolders();
                renderImages(images.images, folders);
                initializeViews();
            }
        } catch (error) {
            alert("Error adding folder:", error);
        }
    });

    addFolderButton.addEventListener('click', async () => {
        page = 1
        try {
            const path = await window.dialog.openFolder();
            if (path[0]) {
                const folderId = await addFolder(path[0]);
                await scan(folderId);
                const images = await getImages(page);
                const folders = await getFolders();
                renderImages(images.images, folders);
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
        page = 1;
        const sortedImages = await getSortedimages(colorWheel.rgb, page);
        sorted = true;
        const folders = await getFolders();
        renderImages(sortedImages.images, folders)
    });

    await main();
});

async function getSortedimages(color, page) {
    try {
        const response = await axios.post(`http://127.0.0.1:8080/api/sort/?page=${page}&orientation=horizontal`, {color: color});
        console.log(page);
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.log(error);
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

async function getImages(page) {
    try {
        const response = await axios.get(`http://127.0.0.1:8080/api/image/?page=${page}`);
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

function renderImages(images, folders, clear=true) {
    const imagesContainer = document.querySelector(".images");
    if (clear) {
        imagesContainer.innerHTML = '';
    }
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
