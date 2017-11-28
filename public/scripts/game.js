const DOMAIN = 'boredgames.io'

class Game extends React.Component {

  constructor(props) {
    super(props)

    const params = location.search.substr(1).split("&")
    const gameId = params[0].split("=")[1]
    const gameCode = params[1].split("=")[1]
    this.state = {
      id: gameId,
      code: gameCode,
      tiles: null
    }

    this.getCurrentState = this.getCurrentState.bind(this)
    this.setCurrentState = this.setCurrentState.bind(this)
    this.getCurrentState()
  }

  getCurrentState() {
    $.get({
      url: `http://${DOMAIN}/game/${this.state.id}/${this.state.code}`,
      success: function(data) {
        this.setCurrentState(data)
        setTimeout(this.getCurrentState, 3000)
      }.bind(this)
    }).fail(function(error) {
      alert('Invalid game ID or game code')
    })
  }

  setCurrentState(data) {
    this.setState({
      assassin: new Set(data.assassin),
      blue: new Set(data.blue),
      guessed: new Set(data.guessed),
      isSpymaster: data.isSpymaster,
      neutral: new Set(data.neutral),
      red: new Set(data.red),
      tiles: new Set(data.tiles),
      blueScore: parseInt(data.blueScore),
      redScore: parseInt(data.redScore)
    })
  }

  render() {
    if (this.state.tiles === null) {
      return(<p>Loading</p>)
    }

    let rows = []
    const tileList = Array.from(this.state.tiles)
    for (let i = 0; i < 5; i++) {
      let squareRow = []
      for (let j = 0; j < 5; j++) {
        const word = tileList[i * 5 + j]
        const square = <Square
          code={this.state.code}
          data={word}
          gameId={this.state.id}
          isAssassin={this.state.assassin.has(word)}
          isBlue={this.state.blue.has(word)}
          isGuessed={this.state.guessed.has(word)}
          isNeutral={this.state.neutral.has(word)}
          isRed={this.state.red.has(word)} />
        squareRow.push(<td>{square}</td>)
      }
      rows.push(<tr>{squareRow}</tr>)
    }

    return(
      <table>
        <tbody>
          <tr>
            <td>
              <table>
                <tbody>
                  {rows}
                </tbody>
              </table>
            </td>
            <td>
              <GameScore blueScore={this.state.blueScore}
                         redScore={this.state.redScore} />
            </td>
          </tr>
        </tbody>
      </table>
    )
  }
}

ReactDOM.render(
  <Game />,
  document.getElementById('content')
);
