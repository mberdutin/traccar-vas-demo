import { Button, Typography } from '@mui/material';
import { makeStyles } from 'tss-react/mui';
import { useTranslation } from '../common/components/LocalizationProvider';

const useStyles = makeStyles()((theme) => ({
  root: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: theme.spacing(1),
    padding: theme.spacing(1, 1.5),
    borderBottom: '1px solid',
    borderColor: theme.palette.divider,
    backgroundColor: theme.palette.background.paper,
    flexShrink: 0,
    minWidth: 0,
  },
  count: {
    display: 'flex',
    alignItems: 'center',
    gap: theme.spacing(1),
    minWidth: 0,
  },
  dot: {
    width: theme.spacing(1),
    height: theme.spacing(1),
    borderRadius: '50%',
    backgroundColor: theme.palette.info.main,
    flexShrink: 0,
  },
}));

const HiddenDevicesBar = ({ count, onShowAll }) => {
  const { classes } = useStyles();
  const t = useTranslation();

  return (
    <div className={classes.root} data-testid="hiddenDevicesBar" role="status">
      <div className={classes.count}>
        <span className={classes.dot} aria-hidden="true" />
        <Typography variant="body2" noWrap>
          {`${t('deviceHidden')}: ${count}`}
        </Typography>
      </div>
      <Button
        size="small"
        variant="outlined"
        color="primary"
        onClick={onShowAll}
        aria-label={t('deviceShowAll')}
      >
        {t('deviceShowAll')}
      </Button>
    </div>
  );
};

export default HiddenDevicesBar;
