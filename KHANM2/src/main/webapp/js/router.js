import util from './util.js';

const main = document.querySelector('main');
const routes = Object.create(null);

export default {
	register: function(path, component) {
		if (!component['render'] || !(component['render'] instanceof Function)) {
			throw `Component '${path}' must contain a render function!`;
		}
		routes[path] = component;
	},

	navigate: function(path, param) {
		path += param ? '/' + param : '';
		if (location.hash !== '#' + path) {
			location.hash = path;
		} else {
			render();
		}
	}
};

function render() {
	const hash = decodeURI(location.hash).replace('#/', '').split('/');
	const path = '/' + (hash[0] || '');
	if (!routes[path]) {
		replaceView(util.createNodeFromHTML('<h2>404 - Not Found</h2><p>Sorry, page not found!</p>'));
		return;
	}
	const component = routes[path];
	const param = hash.length > 1 ? hash[1] : '';
	const view = component.render(param);
	replaceView(view);
	document.title = "Bookstore" + (component.getTitle ? " - " + component.getTitle() : "");
}

function replaceView(view) {
	main.firstElementChild.remove();
	main.append(view);
}

window.addEventListener('hashchange', render);
