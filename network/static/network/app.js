document.addEventListener('DOMContentLoaded', function() {

    // Edit Post

    document.querySelectorAll('.edit_Button').forEach(btn => {

        btn.onclick = function () {
           /// console.log("clicked" + btn.dataset.post_id)
            let id = btn.dataset.post_id;
            btn.style.display = 'none'
            let content_div = document.querySelector(`#post-content-${btn.dataset.post_id}`);
            let contents = content_div.querySelector('.article-content').innerText;
            content_div.querySelector('.article-content').style.display = 'none';

            var edit_text = document.createElement("textarea");
            edit_text.style.width = '100%';
            edit_text.setAttribute('form', 'editform');
            edit_text.value = contents;
            content_div.appendChild(edit_text);
            var edit_form = document.createElement("form");
            edit_form.setAttribute('id', 'editform');

            const save_edit = document.createElement('input');
            save_edit.type = 'submit';
            save_edit.value = 'Save';
            save_edit.classList.add('btn', 'btn-primary');

            const cancel_edit = document.createElement('button');
            cancel_edit.type = 'button';
            cancel_edit.textContent = 'Cancel'
            cancel_edit.classList.add('btn', 'btn-danger');

            edit_form.appendChild(save_edit);
            edit_form.appendChild(cancel_edit);
            content_div.appendChild(edit_form);

            cancel_edit.addEventListener("click", function() {
                edit_form.style.display = 'none';
                edit_text.style.display = 'none';
                content_div.querySelector('.article-content').style.display = 'block';
                btn.style.display = 'block'
            });

            edit_form.onsubmit = () => {
                fetch('/edit/' + id, {
                    method: 'PUT',
                    body: JSON.stringify({
                        content: edit_text.value
                    })
                })
                .then(result => {
                    if (result.error) {
                        console.log(`Error editing post: ${result.error}`);
                    } else {
                        edit_form.style.display = 'none';
                        edit_text.style.display = 'none';
                        content_div.querySelector('.article-content').style.display = 'block';
                        content_div.querySelector('.article-content').innerHTML = edit_text.value;
                        btn.style.display = 'block'
                    }
                })
            }
             
        }

    })

    // Like post 

    document.querySelectorAll('.like-form').forEach(form => {

        form.onsubmit = function (e) {
            e.preventDefault();
            const post_id = this.getAttribute('id');
            var url = this.getAttribute('action');
            const likeText = document.querySelector(`.like-btn-${post_id}`)
            var like_count = document.querySelector(`.like-count-${post_id}`)
            fetch(url)
            .then(res => res.json())
            .then(post => {
                if (post.liked) {
                    likeText.innerHTML = 'Unlike'
                    like_count.innerHTML = post.like_total

                } else {
                    likeText.innerHTML = 'Like'
                    like_count.innerHTML = post.like_total
                }
            })
    
        }

    })






})


                                                                                                                              