import util from '../util.js';
import store from '../store.js';

export default {
    render: function(isbn) {
        const book = store.getBook(isbn);
        return util.loadTemplate('book', view => initView(view, book));
    }
};

function initView(view, book) {
    view.querySelector('.title').textContent = book.title;
    view.querySelector('.subtitle').textContent = book.subtitle;
    view.querySelector('.isbn').textContent = book.isbn;
    view.querySelector('.price').textContent = book.price;

    translateText(book.title)
        .then(translatedTitle => {
            view.querySelector('.title').textContent = translatedTitle;
        })
        .catch(() => {
            view.querySelector('.title').style.fontStyle = 'italic';
        });

    translateText(book.subtitle)
        .then(translatedSubtitle => {
            view.querySelector('.subtitle').textContent = translatedSubtitle;
        })
        .catch(() => {
            view.querySelector('.subtitle').style.fontStyle = 'italic';
        });
}

function translateText(text) {
    return fetch(`https://locher.ti.bfh.ch/services/translate?text=${encodeURIComponent(text)}`)
        .then(response => response.text());
}