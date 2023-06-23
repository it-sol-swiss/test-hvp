import util from '../util.js';
import router from '../router.js';

export default {
	render: function(isbn) {
		return util.loadTemplate('order', view => initView(view, isbn));
	}
};

function initView(view, isbn) {
	view.querySelector('[name=isbn]').value = isbn;

	view.querySelector('[data-action=cancel]').addEventListener('click', e => {
		e.preventDefault();
		router.navigate('/');
	});
}

function getFormData() {
	const form = document.forms[0];
	return {
		isbn: form.isbn.value,
		name: form.name.value,
		address: form.address.value
	};
}
