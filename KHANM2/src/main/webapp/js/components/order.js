import util from '../util.js';
import store from '../store.js';
import service from '../service.js';

export default {
	render: function(isbn) {
		const book = store.getBook(isbn);
		return util.loadTemplate('order', view => initView(view, book));
	}
};

function initView(view, book) {
	view.querySelector('.isbn').textContent = book.isbn;
	view.querySelector('.title').textContent = book.title;
	view.querySelector('.price').textContent = book.price;

	view.querySelector('form').addEventListener('submit', e => {
		e.preventDefault();
		const customer = view.querySelector('.customer').value;
		service.ajax('POST', '/api/orders', {isbn: book.isbn, customer: customer})
			.then(order => {
				view.querySelector('form').style.display = 'none';
				view.querySelector('.confirmation').style.display = 'block';
			})
			.catch(error => {
				view.querySelector('.error').style.display = 'block';
			});
	});
}
