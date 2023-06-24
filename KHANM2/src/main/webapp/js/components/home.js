import util from '../util.js';
import store from '../store.js';
import service from '../service.js';
import router from '../router.js';

export default {
	render: function() {
		return util.loadTemplate('home', initView);
	}
};

function initView(view) {

	if (!store.getBooks()) {
		service.getBooks().then(books => {
			store.setBooks(books);
			books.forEach(book => renderBook(view, book));
		});
	} else {
		store.getBooks().forEach(book => renderBook(view, book));
	}
}

function renderBook(view, book) {
	const template =
		`<li>
            <img src="${book.image}" alt="${book.title}"/>
            <h2>${book.title}</h2>
            <h4>${book.author}</h4>
            <span class="price">Fr. ${book.price.toFixed(2)}</span>
            <button class="buy" data-isbn="${book.isbn}">Buy now</button>
        </li>`;

	const li = util.createNodeFromHTML(template);

	li.querySelector('img').addEventListener('click', e => {
		router.navigate('/book', book.isbn);
	});

	li.querySelector('h2').addEventListener('click', e => {
		router.navigate('/book', book.isbn);
	});

	li.querySelector('.buy').addEventListener('click', e => {
		router.navigate('/order', book.isbn);
	});

	view.querySelector('ul').append(li);
}
``
