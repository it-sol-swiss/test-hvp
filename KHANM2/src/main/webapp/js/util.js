const TEMPLATE_ROOT = 'templates/';
const TEMPLATE_EXT  = '.html';

export default {
	loadTemplate: function(template, cb) {
		const view = document.createElement('div');
		fetch(TEMPLATE_ROOT + template + TEMPLATE_EXT)
			.then(response => {
				if (!response.ok) throw response;
				return response.text();
			}).then(template => {
			view.innerHTML = template;
			if (cb instanceof Function) cb(view);
		}).catch(error => {
			view.innerHTML = `<p class="danger">Loading template failed!</p>`;
		});
		return view;
	},

	createNodeFromHTML: function(html) {
		const template = document.createElement('template');
		template.innerHTML = html.trim();
		return template.content.firstChild;
	}
};
