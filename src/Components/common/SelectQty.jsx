import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import FormControl from "@material-ui/core/FormControl";
import Select from "@material-ui/core/Select";
import { connect } from "react-redux";
import { changeQuantity, calTotalBill } from "../../Redux/Employee/actions";

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 50,
  },
}));

const SelectQty = (props) => {
  const classes = useStyles();
  const { quantity, item, changeQuantity, calTotalBill } = props;
  const [qty, setQty] = React.useState(Number(quantity));

  const handleChange = (event) => {
    setQty(event.target.value);
    changeQuantity([item[1], event.target.value]);
    setTimeout(() => {
      calTotalBill();
    }, 10);
  };

  let selectItems = [];
  if (item[3] >= 10) {
    for (let i = 1; i <= 10; i++) {
      selectItems.push(
        <MenuItem key={i} value={i}>
          {i}
        </MenuItem>
      );
    }
  } else if (item[3] < 10) {
    for (let i = 1; i <= item[3]; i++) {
      selectItems.push(
        <MenuItem key={i} value={i}>
          {i}
        </MenuItem>
      );
    }
  }

  return (
    <FormControl className={classes.formControl}>
      <InputLabel id="qty">Qty</InputLabel>
      <Select labelId="qty" value={qty} onChange={handleChange}>
        {selectItems}
      </Select>
    </FormControl>
  );
};

const mapStateToProps = (state) => ({});

const mapDispatchToProps = (dispatch) => ({
  changeQuantity: (payload) => dispatch(changeQuantity(payload)),
  calTotalBill: (payload) => dispatch(calTotalBill(payload)),
});

export default connect(mapStateToProps, mapDispatchToProps)(SelectQty);
