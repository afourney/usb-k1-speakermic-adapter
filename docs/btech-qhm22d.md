# BTECH QHM22D: wiring test and repair

[Back to the build guide](../README.md)

These instructions apply to the **BTECH QHM22D** used in this build. Its yellow and brown cable wires arrived reversed, putting the PTT return on the speaker signal contact. Test your unit before connecting it; do not swap wires on a unit that already passes. This repair is not a general requirement for K1 speaker mics.

On this handset, **PTT Main** is the large side button (`PTT1` / `D2`), and **PTT Secondary** is the small top button (`PTT2` / `D3`). See the [K1 accessory pinout](../README.md#k1-accessory-pinout) for the contact assignments and original wiring sources.

## 1. Test the speaker mic before building

The defect is easy to miss: the internal speaker can still make sound with reversed leads. The important problem here is where the PTT switch connects, not just acoustic polarity.

1. Disconnect the handset from everything: radio, adapter, USB, and any external earphones.
2. Set the meter to resistance, preferably its lowest useful range. Touch the probes together and note the lead resistance.
3. Identify the **2.5 mm tip**, **2.5 mm sleeve**, and **3.5 mm sleeve** on the handset's radio plug.
4. Measure between the two sleeves while holding the PTT button associated with the **3.5 mm sleeve**. On a dual-button handset, try each button separately to identify it; this guide calls that input PTT1.
5. Keep that same button pressed and measure between the **2.5 mm tip** and **3.5 mm sleeve**.
6. Compare the pair of readings with the table. Use actual resistance values: a continuity buzzer may beep for both 0 Ω and 8 Ω.

### Test 1: sleeve to sleeve

Hold PTT1. Touch the **black probe to the 3.5 mm sleeve** and the **red probe to the 2.5 mm sleeve**. A correctly wired unit reads approximately **0 Ω**; the reversed unit reads the speaker's resistance, approximately **8–9 Ω**.

[![Test 1 probe placement: 3.5 mm sleeve to 2.5 mm sleeve, with correct and reversed resistance readings](../hardware/testing/qhm22d-test-1.png)](../hardware/testing/qhm22d-test-1.svg)

### Test 2: move one probe to the tip

Keep **the same PTT button held** and the **black probe on the 3.5 mm sleeve**. Move only the **red probe to the 2.5 mm tip**. The readings should exchange: approximately **8–9 Ω** when correctly wired, or approximately **0 Ω** on the reversed unit.

[![Test 2 probe placement: 3.5 mm sleeve to 2.5 mm tip, with correct and reversed resistance readings](../hardware/testing/qhm22d-test-2.png)](../hardware/testing/qhm22d-test-2.svg)

The drawings show the **radio-end plugs**, not the handset's headphone socket. Touch one exposed metal segment with each probe; avoid bridging a black insulating band. The probe colours are for clarity—either polarity works for these two resistance checks. Click either diagram to open its editable SVG.

| Measurement, with PTT1 held | Correct wiring | Reversed wiring on this unit |
| --- | --- | --- |
| 2.5 mm **sleeve** ↔ 3.5 mm sleeve | Approximately **0 Ω** plus probe/contact resistance | Approximately **8 Ω**, through the speaker |
| 2.5 mm **tip** ↔ 3.5 mm sleeve | Approximately **8 Ω**, through the speaker | Approximately **0 Ω** |

The speaker in this build measured around **8–9 Ω**; treat that as a recognizable speaker-coil reading, not a precision acceptance limit. Swapping the meter probes does not change which test is which—the distinction is **tip versus sleeve on the 2.5 mm plug**.

Release PTT1 and verify that the sleeve-to-sleeve short disappears. Also identify PTT2 by testing **3.5 mm tip ↔ 2.5 mm sleeve**: the repaired handset should change from open/high resistance to near zero when its other button is held. If the switching or resistance pattern differs substantially, trace the accessory before using this wiring plan.

### Reports of the same problem

- [Amazon review: “repair the factory defect and then it works great,” September 4, 2022](https://www.amazon.com/gp/customer-reviews/RETJVNP2EQFWO). The reviewer describes reversed speaker leads and loss of PTT when external headphones are connected. Amazon may require sign-in; the review's supplied screenshot was used as a reference and is not redistributed here.
- [Independent repair report: “Comms at Home, QHM22D question”](https://www.reddit.com/r/Baofeng/comments/123nzs1/comms_at_home_qhm22d_question/). The discussion links that exact Amazon review, and the owner reports that the repair worked.
- [Earlier first-hand symptom report](https://www.reddit.com/r/Baofeng/comments/lg8wdt/help_baofeng_qhm22d_dual_ptt_speaker_mic_stops/). The original post is deleted, so the remaining thread provides limited context; it is not proof of a particular internal fault.
- [Adam Fourney's review on BTECH's product page](https://baofengtech.com/product/qhm22d/#reviews), September 8, 2026, records this build's resistance readings and repair. This is the same unit documented here, not an additional independent sample.

These are reports about particular units, not evidence that every QHM22D is wired incorrectly.

## 2. Repair the yellow/brown reversal, if present

Only do this if your measurements identify the reversal. Returning a defective unit is also an option.

1. With the handset completely disconnected, remove the two screws on its back.
2. Carefully open the housing without pulling on the speaker or microphone leads. Photograph the original wiring.
3. Locate the **lower row of cable connections** on the PCB, beside the cable entry. On the photographed board the labels read `SP−`, `SP+`, `PTTB`, `MIC+`, and `PTTA`.
4. Desolder the **yellow** lead from `SP−` and the **brown** lead from `SP+`. Let the solder melt before lifting each wire; do not pull up a pad.
5. Reconnect **brown to `SP−`** and **yellow to `SP+`**. Leave the adjacent green, red, and black cable wires alone. Leave the separate red/black wires to the speaker and microphone at the top of the board alone too.
6. Inspect for solder bridges, loose strands, damaged insulation, and a secure cable entry. Wire colours can change between revisions; the labels and measurements take precedence.
7. Repeat both PTT1 resistance measurements and the PTT2 switching check **before reconnecting anything powered**. The two PTT1 readings should now match the correct-wiring column.
8. Refit the housing without pinching wires or disturbing its seal.

| Before: factory reversal on this unit | After: corrected cable connections |
| --- | --- |
| ![Before repair: yellow on SP minus, brown on SP plus](images/qhm22d-before.jpg) | ![After repair: brown on SP minus, yellow on SP plus](images/qhm22d-after.jpg) |
| `SP−`: yellow · `SP+`: brown | `SP−`: brown · `SP+`: yellow |

Both pictures show the actual handset used in this project. The swap is on the **incoming cable pads at the bottom**, not the speaker's own two wires at the top.

[Continue with adapter assembly](../README.md#2-prepare-the-cables-and-connector-breakout)
