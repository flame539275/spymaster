class Square extends React.Component {
  constructor(props) {
    super(props)
    this.handleClick = this.handleClick.bind(this)
  }

  handleClick() {
    if (!this.props.isGuessed) {
      if (confirm(`Guess ${this.props.data}?`) === true) {
        const id = this.props.gameId
        const code = this.props.code
        const word = this.props.data
        $.post({
          url: `http://localhost:3000/guess/${id}/${code}/${word}`
        })
      }
    }
  }

  getColor() {
    if (this.props.isAssassin) {
      return '#808080'
    } else if (this.props.isBlue) {
      return '#3385FF'
    } else if (this.props.isRed) {
      return '#FF6666'
    } else if (this.props.isNeutral) {
      return '#FFCC66'
    }
  }

  render() {
    const buttonStyle = { backgroundColor: this.getColor() }
    return(
      <div style={buttonStyle}
           onClick={this.handleClick}
           className="square"
      > <span className="text"> {this.props.data} </span> </div>
    )
  }
}
