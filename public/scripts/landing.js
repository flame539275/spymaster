const DOMAIN = 'boredgames.io'

class Landing extends React.Component {

  constructor(props) {
    super(props)
    this.state = { gameId: '' }
    
    var txtFile = "../../wordlist.txt"          //maybe filepath needs fixing
    var file = new File(txtFile)
    file.open("r"); // open file with read access
    var wordArray = []
    var i = 0
    while (!file.eof) {
      // store each word in the array
      wordArray[i] = file.readln()
    }
    file.close()
    this.setState({ gameId: wordArray[Math.floor(Math.random() * wordArray.length)] })  

    this.createGame = this.createGame.bind(this)
    this.handleChange = this.handleChange.bind(this)
    this.onCreateGame = this.onCreateGame.bind(this)
    this.renderForm = this.renderForm.bind(this)
  }

  createGame() {
    $.post({
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
      data: JSON.stringify({ game_id: this.state.gameId }),
      url: `http://${DOMAIN}/new_game`,
      success: this.onCreateGame
    }).fail(function(data) {
      const response = data.responseJSON
      if (response.error === "Game with given game_id already exists.") {
        window.location.href = `http://${DOMAIN}/game?id=${response.game_id}`
      }
    })
  }

  handleChange(event) {
    this.setState({ gameId: event.target.value })
  }

  onCreateGame(data) {
    const id = data.game_id
    const code = data.spymaster_code
    window.location.href = `http://${DOMAIN}/game?id=${id}&code=${code}`
  }

  renderForm() {
    return(
      <form onSubmit={this.createGame}>
        <h2>Codenames</h2>
        <p>This app allows you to play Codenames across multiple devices with a shared board. To create a new game or join an existing game, enter a game identifer and click 'Go.'</p>
        <input type="text"
               name="gameId"
               value={this.state.gameId}
               onChange={this.handleChange} />
        <input type="submit" value="Go" />
      </form>
    )
  }

  render() {
    return(
      <div>
        {this.renderForm()}
      </div>
    )
  }
}

ReactDOM.render(
  <Landing />,
  document.getElementById('content')
)
