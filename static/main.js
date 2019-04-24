function changeVote(voteValue, dataType, id) {
    fetch(`/${dataType}/${id}/vote`, {
      method: "PUT",
      headers: {"Content-type": "application/json"},
      body: JSON.stringify({voteValue})
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById(`${dataType}-vote-${id}`).textContent = data.vote_number
    })
    .catch(err => console.log(err))
}

const questionVoteUp = question_id => changeVote(1, "question", question_id);
const questionVoteDown = question_id => changeVote(-1, "question", question_id);
const answerVoteUp = answer_id => changeVote(1, "answer", answer_id);
const answerVoteDown = answer_id => changeVote(-1, "answer", answer_id);
