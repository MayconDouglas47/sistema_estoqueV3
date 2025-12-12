/* main.js - comportamentos do sidebar e interações */


(function(){
	// Simplified main.js: sidebar is fixed; no collapse/overlay functionality.
	const links = document.querySelectorAll('#sidebar .nav-link');
	links.forEach(link=>{
		try{
			if(link.href === window.location.href){
				link.classList.add('active');
			}
		}catch(e){}
	});
})();