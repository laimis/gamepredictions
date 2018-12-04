select team, name, sum(fgm * 2) + sum(tpm * 3) + sum(ftm) + sum((oreb+dreb)*1.2) + sum(assists * 1.5) + sum(blocks * 3) + sum(steals * 3) + sum(turnovers * -1) from gamerows gr
join games g on g.id = gr.gameid
where g.date > current_date - 20
and team in (
'dal',
'lac',
'mia',
'uta',
'phi',
'mem',
'sas',
'por')
group by team, name
order by sum(fgm * 2) + sum(tpm * 3) + sum(ftm) + sum((oreb+dreb)*1.2) + sum(assists * 1.5) + sum(blocks * 3) + sum(steals * 3) + sum(turnovers * -1) desc