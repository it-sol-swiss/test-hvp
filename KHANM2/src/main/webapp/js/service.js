const BASE_URL = 'api/';

export default {
	getBooks: function(query) {
		query = query ? '?query='+query : '';
		return ajax(BASE_URL + 'books' + query, {
			method: 'GET',
			headers: { 'Accept': 'application/json' }
		});
	}
};


function ajax(url, options) {
	return fetch(url, options)
		.then(response => {
			if (!response.ok) throw response;
			return response.headers.get('Content-Type') === 'application/json' ? response.json() : response;
		})
}
